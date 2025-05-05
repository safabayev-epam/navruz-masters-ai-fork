# Customer Support Chatbot

A Gradio-based Retrieval-Augmented Generation (RAG) AI chatbot that:

* Answers user questions by retrieving and citing content from your PDF documents
* Maintains conversational context for follow-up queries
* Suggests and creates support tickets in Jira when answers aren’t found
* Is configurable via environment variables and deployable on Hugging Face Spaces

---

## Repository Structure

```
customer-support-bot/
├── app.py             # Main Gradio app & interaction logic
├── ingest.py          # Document ingestion: chunking, embedding, vectorstore persistence
├── qa_bot.py          # QA chain logic: retrieval + LLM answer generation (with citations)
├── ticketing.py       # Jira integration: client setup & ticket-creation helper
├── config.py          # Configuration & environment-variable loading
├── requirements.txt   # Python dependencies
├── runtime.txt        # (optional) Python version pin for Spaces
├── README.md          # This file
├── data/              # Drop your source PDFs here
│   ├── manual.pdf
│   ├── guide.pdf
│   └── policy.pdf
└── db/                # Persisted vector-store index (after running ingest.py)
```

---

## Prerequisites

* Python 3.10+ (pin via `runtime.txt` if needed)
* An OpenAI API key for embeddings & LLM (or configure a local HF model)
* A Jira account with API token and project to create issues
* Your PDF documents placed in `data/`

---

## Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/your-username/customer-support-bot.git
   cd customer-support-bot
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

Set the following environment variables (e.g. in a `.env` file or via your shell):

```bash
# OpenAI
export OPENAI_API_KEY="your-openai-api-key"

# Jira
export JIRA_EMAIL="your.email@example.com"
export JIRA_API_TOKEN="your-jira-api-token"
export JIRA_SERVER_URL="https://your-domain.atlassian.net"
export JIRA_PROJECT_KEY="YOURPROJ"
```

(Optional) Configure company info in `config.py`:

* `COMPANY_NAME`
* `SUPPORT_EMAIL`
* `SUPPORT_PHONE`

---

## Data Ingestion

1. Place your PDF files in the `data/` directory.
2. Run the ingestion script to build the vector index:

   ```bash
   python ingest.py
   ```
3. A Chroma index will be persisted under `db/`.

---

## Running Locally

Start the Gradio app:

```bash
python app.py
```

Open your browser at the printed local URL (e.g., `http://127.0.0.1:7860`).

---

## Deployment on Hugging Face Spaces

1. Create a new Space on Hugging Face with the **Gradio** SDK.
2. Push this repo to your Space.
3. In the Space settings, add Secrets for the same environment variables:

   * `OPENAI_API_KEY`
   * `JIRA_EMAIL`
   * `JIRA_API_TOKEN`
   * `JIRA_SERVER_URL`
   * `JIRA_PROJECT_KEY`
4. The Space will install dependencies from `requirements.txt` and launch `app.py` automatically.

---

## Usage

* **Ask a question**: The bot will search your documents and reply with an answer and citation (e.g., `manual.pdf (p.10)`).
* **No answer found**: The bot will prompt to create a Jira ticket. Reply `yes` to proceed or `no` to skip.
* **Ticket flow**: Provide your name, email, title, and issue description. The bot will submit a ticket and return the ticket key.

---

## Troubleshooting

* If the app fails to start, ensure all environment variables are set and dependencies installed.
* For large PDFs, ingestion may take time—monitor console logs for progress.
* Verify your Jira credentials and project key if ticket creation fails.

---

## License

MIT License © Navruz Safabayev
