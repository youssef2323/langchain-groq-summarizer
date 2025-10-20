# Summarize Text from YouTube or Website (Streamlit + LangChain + Groq)

## Overview
A minimal Streamlit app that takes a **YouTube** or **website** URL, loads the content, and generates a **~300-word summary** using a Groq-hosted LLM via LangChain. Enter your **Groq API key** in the sidebar, paste a URL, and click **“Summarize the Content”**. :contentReference[oaicite:0]{index=0}

---

## Screenshots

![](screenshots/01-home.png)
![](screenshots/02-url.png)
![](screenshots/03-youtube.png)
![](screenshots/04-website.png)
![](screenshots/05-summary.png)

> Put PNGs in a top-level `screenshots/` folder (use simple names like above).

---

## ✨ Features
- **YouTube support**: extracts video ID and fetches auto-transcript with `youtube-transcript-api`. :contentReference[oaicite:1]{index=1}  
- **Website support**: loads page text via `UnstructuredURLLoader` (with desktop user-agent and SSL verify off). :contentReference[oaicite:2]{index=2}  
- **LLM**: `ChatGroq(model="openai/gpt-oss-20b")`, key entered in the sidebar. :contentReference[oaicite:3]{index=3}  
- **Prompting**: `PromptTemplate` asking for a **300-word** summary; `load_summarize_chain(chain_type="stuff")`. :contentReference[oaicite:4]{index=4}  
- **Validation & UX**: URL validated with `validators`; clear errors for missing key/URL or missing YT transcript. :contentReference[oaicite:5]{index=5}

---

## Tools & Technologies
Streamlit · LangChain (`ChatGroq`, `load_summarize_chain`, `PromptTemplate`, `Document`) · `youtube-transcript-api` · `validators` · `langchain_community.document_loaders.UnstructuredURLLoader`. :contentReference[oaicite:6]{index=6}

---

## How It Works
1. **URL input**: user enters a YouTube or website URL; the app validates it. :contentReference[oaicite:7]{index=7}  
2. **Loader**:
   - If YouTube: parse `v` or shortlink ID → fetch transcript → wrap as `Document`.  
   - If website: fetch with `UnstructuredURLLoader` using headers. :contentReference[oaicite:8]{index=8}
3. **Summarization**: build a 300-word summary prompt and run `load_summarize_chain` with `ChatGroq`. :contentReference[oaicite:9]{index=9}
4. **Output**: show the summary in the UI, with spinner + success state. :contentReference[oaicite:10]{index=10}

---

## Configuration
- **Groq API Key**: paste in the sidebar (masked). :contentReference[oaicite:11]{index=11}  
- **Model**: default `openai/gpt-oss-20b`; change in code if desired. :contentReference[oaicite:12]{index=12}

---

## Troubleshooting
- **“Please enter a valid URL.”** → ensure the URL passes basic validation. :contentReference[oaicite:13]{index=13}  
- **YouTube transcript not found** → some videos disable transcripts; the app shows an error and stops. :contentReference[oaicite:14]{index=14}  
- **Website load failed** → page may block scraping or require JS; try another URL. :contentReference[oaicite:15]{index=15}

---

## License
MIT

