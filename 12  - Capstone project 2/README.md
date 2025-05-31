---
title: Customer Support AI
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: streamlit
app_file: app.py
pinned: false
license: apache-2.0
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# Huggingface Link

https://huggingface.co/spaces/safabayev/support-chatbot

# Support Chatbot for PDFs

A Streamlit-based web application that lets you upload one or more PDFs and chat with them via OpenAI embeddings. Users can ask questions, see which pages were referenced, and (if an answer can’t be found) create a Jira ticket to request missing information.

---

## Table of Contents

1. [Features](#features)  
2. [Prerequisites](#prerequisites)  
3. [Project Structure](#project-structure)  
4. [Installation](#installation)  
5. [Configuration & Secrets](#configuration--secrets)  
6. [Running Locally](#running-locally)  
7. [Docker Usage](#docker-usage)  
8. [Deploying on Hugging Face Spaces](#deploying-on-hugging-face-spaces)  
9. [How It Works (High-Level)](#how-it-works-high-level)  
10. [File Summaries](#file-summaries)  
11. [Troubleshooting](#troubleshooting)  
12. [Contributing](#contributing)  
13. [License](#license)  

---

## Features

- **PDF Upload & Processing**  
  Upload any number of PDFs; code splits pages into overlapping text chunks using LangChain’s RecursiveCharacterTextSplitter.

- **Embedding & Vector Store**  
  Uses OpenAI’s text-embedding-3-small model to embed chunks, stores them in FAISS, and builds a retrieval chain.

- **Conversational UI**  
  A chat interface with custom CSS, user/bot avatars, and support for chat history.

- **Source-Page References**  
  Whenever the bot cites information, it displays “Referenced pages” (e.g., mydoc.pdf – pages 4, 7).

- **Jira Ticketing for Unanswered Questions**  
  If the assistant returns a “not found” response, users can click a button to create a Jira Task (with summary, description, and their email) to request missing content.

- **Docker-Ready**  
  A Dockerfile is provided so you can build and run this app as a container.

- **Hugging Face Spaces Deployment**  
  Instructions and Docker settings are included for easy deployment on the Hugging Face Spaces platform (Docker mode).

---

## Prerequisites

1. **Python 3.10+** (we recommend using a venv or Conda environment)  
2. **Docker Engine** (if you plan to build/run via Docker)  
3. **Hugging Face account** (for deploying to Spaces, if desired)  
4. **Jira account & API token** (optional, only needed for ticket creation)  
5. **OpenAI API Key** (required to compute embeddings and run the LLM)  

---

## Project Structure

support-chatbot/
├── app.py  
├── constants.py  
├── requirements.txt  
├── Dockerfile  

├── ui/  
│   ├── __init__.py  
│   ├── chat_renderer.py        # Renders chat messages + “create Jira” logic  
│   └── jira_renderer.py        # Renders the Jira form in Streamlit  

└── utils/  
    ├── __init__.py  
    ├── jira.py                 # create_jira_ticket() helper  
    ├── pdf_processing.py       # get_pdf_chunks()  
    ├── vectorstore.py          # get_vectorstore(), get_conversation_chain()  
    └── prompts.py              # STRICT_PROMPT (if separated; otherwise in constants.py)  

- **app.py**: Entry point. Configures Streamlit, handles file uploads, invokes processing, and ties together UI modules.  
- **constants.py**: Global CSS, HTML templates, Jira settings, “not found” messages, and the strict prompt template.  
- **requirements.txt**: Pinned Python dependencies.  
- **Dockerfile**: Instructions to build a container that runs the Streamlit app on port 80.  
- **ui/**: Contains all Streamlit UI rendering logic—kept separate from core utilities.  
- **utils/**: Core helpers for PDF reading, chunking, vector store creation, conversation chain creation, and Jira interaction.

---

## Installation

1. **Clone this repository**  
   git clone https://github.com/<your-username>/support-chatbot.git  
   cd support-chatbot  

2. **Create and activate a virtual environment**  
   python3.10 -m venv .venv  
   source .venv/bin/activate   # macOS/Linux  
   .venv\Scripts\activate    # Windows PowerShell  

3. **Install dependencies**  
   pip install --upgrade pip  
   pip install -r requirements.txt  

4. **Verify that streamlit, PyPDF2, langchain, etc. are installed**  
   python -c "import streamlit, PyPDF2, langchain; print('Dependencies OK')"

---

## Configuration & Secrets

This app expects two secrets to be set via Streamlit’s secrets mechanism (or as environment variables):

1. **OPENAI_API_KEY**  
   - Needed for OpenAIEmbeddings and ChatOpenAI.  
   - On your local machine, you can create a file at ~/.streamlit/secrets.toml or use environment variables.  

2. **JIRA_API_TOKEN**  
   - Used by utils/jira.py to authenticate when creating a ticket in Jira.  
   - You must also have JIRA_USERNAME (your Atlassian-username/email) and JIRA_PROJECT_KEY defined in constants.py.  

### Using ~/.streamlit/secrets.toml

Create (or edit) the file:

# ~/.streamlit/secrets.toml

# OpenAI key (e.g. sk-XXXXXXXXXX)  
OPENAI_API_KEY = "sk-your_openai_api_key_here"

# Jira API token (Base64 username:token is handled internally by the app)  
JIRA_API_TOKEN = "your_jira_api_token_here"

> **Note:** If you’re deploying to Hugging Face Spaces, you’ll add OPENAI_API_KEY and JIRA_API_TOKEN in the “Secrets” section of the Space’s settings page. You do not commit secrets.toml to Git.

---

## Running Locally

1. **Start Streamlit**  
   In your project root (where app.py lives), run:  
   streamlit run app.py  

2. **Access the app**  
   Open your browser and navigate to the URL displayed (typically http://localhost:8501).  

3. **Upload PDFs & Chat**  
   - Use the sidebar → “Upload your PDFs here” to select one or more .pdf files.  
   - Click Process. You’ll see a confirmation if processing succeeds.  
   - In the main panel, type a question and click Ask.  
   - If your question is answered, you’ll see the answer + “Referenced pages: …”.  
   - If the bot says “I don’t know” (or a similar not-found message), a “📝 Create Jira Ticket” button appears.  
     - Click it, fill in your email/summary/description, then submit to create a Jira task.

---

## Docker Usage

A Dockerfile is provided so you can build and run this app in a container. This is recommended for Hugging Face Spaces or any Docker‐hosted environment.

### 1. Build the image

docker build -t support-chatbot:latest .

- This installs all OS packages (via apt) and Python dependencies (via requirements.txt), then copies your code.

### 2. Run the container locally

docker run --rm -p 8501:80                                 \  
    -e OPENAI_API_KEY="sk-your_openai_key_here"           \  
    -e JIRA_API_TOKEN="your_jira_api_token_here"          \  
    support-chatbot:latest

- -p 8501:80 maps port 80 in the container (where Streamlit listens) to localhost:8501 on your host.  
- The -e flags set environment variables inside the container (equivalent to Streamlit secrets).  
- After startup, open http://localhost:8501.

> **Tip:** To test Hugging Face’s $PORT behavior, run:  
> docker run --rm -e PORT=80 -e OPENAI_API_KEY="..." -e JIRA_API_TOKEN="..." -p 8501:80 support-chatbot:latest  
> Your app’s Docker CMD reads ${PORT:-80} so it will bind to port 80 properly.

---

## Deploying on Hugging Face Spaces

1. **Create a new Space** on Hugging Face (choose “Docker” as the SDK).  
2. **Push your repository** (with this Dockerfile and README) to the Space’s Git remote.  
3. **Add Secrets** in the Space settings:  
   - OPENAI_API_KEY  
   - JIRA_API_TOKEN  

   (Those will be available to st.secrets in your Streamlit code automatically.)

4. **Wait for the build** to finish. The Space will launch a container reading your Dockerfile, then start Streamlit on port 80.  

Once live, the Space URL will serve your chatbot.  

---

## How It Works (High-Level)

1. **PDF → Text Chunks**  
   - When you click “Process,” app.py calls get_pdf_chunks() (in utils/pdf_processing.py).  
   - Each PDF page is extracted via PyPDF2.PdfReader, then split into ~900-character windows (200 char overlap) using LangChain’s RecursiveCharacterTextSplitter.  
   - Each chunk is stored alongside metadata ({"pdf_name": "<filename>.pdf", "page": <page number>}).

2. **Chunks → FAISS Vectorstore**  
   - In utils/vectorstore.py, get_vectorstore() uses OpenAIEmbeddings (model=text-embedding-3-small) to embed every chunk.  
   - Those embeddings + metadatas go into a FAISS index.

3. **Querying the LLM**  
   - When you ask a question, handle_userinput() calls conversation_chain = get_conversation_chain(...)  
   - We build a ConversationalRetrievalChain from LangChain with:  
     - ChatOpenAI (model=gpt-4.1-mini)  
     - Our FAISS retriever  
     - A “strict” prompt template (STRICT_PROMPT) that forces the model to use only retrieved context.  
     - A ConversationBufferMemory to store chat history.

   - The chain returns an answer plus a list of “source_documents” (docs containing the text chunks used). We parse their metadata to get “pdf_name, page #.”

4. **Rendering & Jira**  
   - ui/chat_renderer.py shows user messages, bot messages, and “Referenced pages” if present.  
   - If the bot’s answer matches one of our “not found” messages, it surfaces a “📝 Create Jira Ticket” button. Clicking it triggers ui/jira_renderer.py, which opens a form to gather email/summary/description and calls create_jira_ticket() in utils/jira.py.  
   - That function uses your JIRA_USERNAME + JIRA_API_TOKEN (Base64-encoded) to hit Atlassian’s REST API and create a Task under the configured JIRA_PROJECT_KEY.

---

## File Summaries

### app.py

- Streamlit entrypoint  
- Loads CSS (constants.CSS) and HTML templates  
- Initializes st.session_state keys (conversation, chat_history, referenced_pages, jira_feedback)  
- Renders the header, upload sidebar, “Process” button, and question form  
- When “Process” is clicked:  
  1. Clears previous state  
  2. Calls get_pdf_chunks()  
  3. Calls get_vectorstore() → get_conversation_chain()  
  4. Shows a “success” message if everything is ready  
- When a question is submitted: calls handle_userinput(user_question) then re-runs  

### constants.py

- CSS  
- HTML templates: BOT_TEMPLATE & USER_TEMPLATE  
- Jira settings: JIRA_URL, JIRA_USERNAME, JIRA_PROJECT_KEY  
- STRICT_PROMPT: Forces the model to answer only from provided chunks or say “I don’t know.”  
- NOT_FOUND_MESSAGES: A list of exact strings that count as “no answer,” prompting the Jira flow  

### utils/pdf_processing.py

- Extracts text page-by-page, splits into overlapping chunks, and returns a list of { text, metadata }  

### utils/vectorstore.py

- Builds a FAISS vectorstore from text chunks and returns a LangChain conversational retrieval chain with memory  

### utils/jira.py

- Takes a summary & description, uses st.secrets["JIRA_API_TOKEN"], and calls Atlassian’s API to create a new Task  

### ui/chat_renderer.py

- Renders user & bot chat messages, displays “Referenced pages,” and shows “Create Jira Ticket” if needed  

### ui/jira_renderer.py

- Renders a Streamlit form for Jira (email/summary/description) and submits via create_jira_ticket()  

---

## Troubleshooting

- “ModuleNotFoundError: No module named 'langchain_openai'”  
  Ensure imports updated to:  
  from langchain.chat_models import ChatOpenAI  
  from langchain.embeddings.openai import OpenAIEmbeddings  
  and requirements.txt pins a recent LangChain

- Docker build fails on FAISS  
  Install extra system packages (e.g., cmake)  

- Port already in use  
  Change host mapping when running locally (e.g. docker run -p 8502:80 …)

- “JIRA_API_TOKEN not found”  
  Set JIRA_API_TOKEN in ~/.streamlit/secrets.toml (locally) or in HF Spaces Secrets

- “OPENAI_API_KEY not found”  
  Ensure OPENAI_API_KEY is in your secrets file or environment

- Hugging Face: “short_description too long”  
  Trim the first YAML metadata block in README.md so short_description ≤ 60 chars

---

## Contributing

Fork this repo and create a new branch for your feature or bugfix. Ensure code follows the existing project structure: keep UI code in ui/ and helpers in utils/. Update requirements.txt if you add new dependencies. Open a pull request with a clear description of your changes.

---

## License

This project is released under the MIT License. See LICENSE for details.