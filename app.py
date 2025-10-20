import streamlit as st
import validators
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)

# === STREAMLIT SETUP ===
st.set_page_config(
    page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜"
)
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader("Paste a YouTube or Website URL below to generate a summary:")

# === SIDEBAR INPUT ===
with st.sidebar:
    groq_api_key = st.text_input("🔑 Groq API Key", value="", type="password")

# === URL INPUT ===
generic_url = st.text_input(
    "Enter a YouTube or Website URL", label_visibility="visible"
)

# === DEFINE PROMPT TEMPLATE ===
prompt_template = """
Provide a summary of the following content in 300 words:
Content: {text}
"""
prompt = PromptTemplate(input_variables=["text"], template=prompt_template)

# === GROQ MODEL SETUP ===
llm = ChatGroq(model="openai/gpt-oss-20b", groq_api_key=groq_api_key)


# === YOUTUBE VIDEO ID PARSER ===
def get_youtube_video_id(url):
    parsed_url = urlparse(url)
    if "youtu.be" in parsed_url.netloc:
        return parsed_url.path[1:]
    elif "youtube.com" in parsed_url.netloc:
        return parse_qs(parsed_url.query).get("v", [None])[0]
    return None


# === FALLBACK YOUTUBE TRANSCRIPT LOADER ===
def load_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry["text"] for entry in transcript])
        return [Document(page_content=full_text)]
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        st.error(f"No transcript found for this YouTube video.")
        return None
    except Exception as e:
        st.error(f"Failed to load transcript: {e}")
        return None


# === BUTTON ACTION ===
if st.button("Summarize the Content"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please enter both a valid URL and your Groq API key.")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL.")
    else:
        with st.spinner("⏳ Loading and summarizing..."):
            try:
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    video_id = get_youtube_video_id(generic_url)
                    if not video_id:
                        st.error(
                            "Could not extract video ID. Please check the YouTube link."
                        )
                        st.stop()
                    docs = load_youtube_transcript(video_id)
                    if not docs:
                        st.stop()
                else:
                    from langchain_community.document_loaders import (
                        UnstructuredURLLoader,
                    )

                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                        },
                    )
                    docs = loader.load()
                    if not docs:
                        st.error("Failed to load content from the website.")
                        st.stop()

                # Optional: show preview
                st.info("Content loaded successfully. Generating summary...")

                # Run summarization chain
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)
                st.success("✅ Summary:")
                st.write(output_summary)

            except Exception as e:
                st.exception(f"Exception: {e}")
