# utils/pdf_processing.py

import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_pdf_chunks(pdf_docs: list) -> list[dict]:
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "."],
        chunk_size=900,
        chunk_overlap=200,
        length_function=len
    )
    all_chunks = []

    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            for i, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    chunks = text_splitter.split_text(page_text)
                    for chunk_text in chunks:
                        all_chunks.append({
                            "text": chunk_text,
                            "metadata": {
                                "pdf_name": getattr(pdf, "name", "PDF"),
                                "page": i + 1
                            }
                        })
        except Exception as e:
            st.error(f"Error reading {getattr(pdf, 'name', 'a file')}: {e}")
    return all_chunks
