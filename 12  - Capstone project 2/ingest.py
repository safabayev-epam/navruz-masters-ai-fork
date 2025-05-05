import os
import logging
import subprocess

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from config import OPENAI_API_KEY

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

def extract_pages_with_pdftotext(pdf_path: str) -> list[str]:
    """
    Run Poppler's pdftotext to extract an entire PDF to stdout (UTF-8),
    then split on form-feed to get individual pages.
    """
    try:
        # Call pdftotext, capturing raw bytes
        completed = subprocess.run(
            ["pdftotext", "-layout", "-enc", "UTF-8", pdf_path, "-"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        raw = completed.stdout  # bytes
        # Decode as UTF-8, ignoring undecodable bytes
        text = raw.decode("utf-8", errors="ignore")
    except subprocess.CalledProcessError as e:
        logger.error(f"pdftotext error on {pdf_path}: {e.stderr.decode('utf-8', errors='ignore')}")
        return []
    except FileNotFoundError:
        logger.error("pdftotext not found on PATH. Please install Poppler and ensure 'pdftotext' is on your PATH.")
        return []

    # Split pages on form-feed
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    return pages

def ingest_documents(
    pdf_paths: list[str],
    persist_dir: str = "db",
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    batch_size: int = 100
):
    """
    1) Extract each PDF page via pdftotext into Unicode text.
    2) Wrap pages as Documents with source & page metadata.
    3) Split into chunks, embed in batches, and persist to Chroma.
    """
    logger.info(f"Starting ingestion of {len(pdf_paths)} PDF(s).")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    docs = []
    for pdf in pdf_paths:
        name = os.path.basename(pdf)
        logger.info(f"Extracting text from '{name}' with pdftotext…")
        pages = extract_pages_with_pdftotext(pdf)
        logger.info(f"  → {len(pages)} pages extracted.")
        for i, page_text in enumerate(pages, start=1):
            if not page_text.strip():
                continue
            docs.append(Document(
                page_content=page_text,
                metadata={"source": name, "page": i}
            ))

    logger.info(f"Total pages wrapped into Documents: {len(docs)}")

    # Split into chunks
    logger.info("Splitting pages into chunks…")
    chunks = []
    for doc in docs:
        chunks.extend(splitter.split_documents([doc]))
    logger.info(f"Total chunks created: {len(chunks)}")

    # Embed & store
    logger.info("Initializing embeddings and vector store…")
    embed = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectordb = Chroma(persist_directory=persist_dir, embedding_function=embed)

    total_batches = (len(chunks) + batch_size - 1) // batch_size
    logger.info(f"Embedding in {total_batches} batch(es) of up to {batch_size} chunks each.")
    for batch_idx, i in enumerate(range(0, len(chunks), batch_size), start=1):
        batch = chunks[i : i + batch_size]
        logger.info(f"  Batch {batch_idx}/{total_batches}: chunks {i}-{i + len(batch) - 1}")
        vectordb.add_documents(batch)

    # Persist
    logger.info("Persisting vector store to disk…")
    vectordb.persist()
    logger.info(f"Finished ingestion. Vector store saved under '{persist_dir}'.")

if __name__ == "__main__":
    data_dir = "data"
    pdfs = [
        os.path.join(data_dir, f)
        for f in os.listdir(data_dir)
        if f.lower().endswith(".pdf")
    ]
    if not pdfs:
        logger.error(f"No PDF files found in '{data_dir}'. Please add your PDFs and rerun.")
    else:
        logger.info(f"Found PDFs: {pdfs}")
        ingest_documents(pdfs)
