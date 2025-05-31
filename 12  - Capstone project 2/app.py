# app.py

import streamlit as st
from constants import CSS
from ui.chat_renderer import handle_userinput, render_chat
from ui.jira_renderer import render_jira_form
from utils.pdf_processing import get_pdf_chunks
from utils.vectorstore import get_vectorstore, get_conversation_chain

def main():
    st.set_page_config(page_title="PDF Chatbot", page_icon="📚", layout="wide")
    st.write(CSS, unsafe_allow_html=True)

    if "OPENAI_API_KEY" not in st.secrets:
        st.error("OPENAI_API_KEY not found in Streamlit secrets.")
        st.stop()
    openai_api_key = st.secrets["OPENAI_API_KEY"]

    # Initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "referenced_pages" not in st.session_state:
        st.session_state.referenced_pages = []
    if "jira_feedback" not in st.session_state:
        st.session_state.jira_feedback = {}

    st.header("Chat with your PDFs 📚")

    # If there’s no active Jira request, show the question form
    if 'active_jira_request' not in st.session_state:
        with st.form(key="user_question_form"):
            user_question_text = st.text_input(
                "Ask a question about your documents:", label_visibility="collapsed"
            )
            submit_button = st.form_submit_button(label="Ask")

        if submit_button and user_question_text:
            handle_userinput(user_question_text)
            st.rerun()

    # Render existing chat history
    if st.session_state.get("chat_history"):
        render_chat()

    # Always try to render the Jira form (it’ll check internally if it should appear)
    render_jira_form()

    # Sidebar: file upload & processing
    with st.sidebar:
        st.info("""
            Note: This POC project does not use a GPU, so processing large PDFs can take a while.
            The code can easily be upgraded with a better model or hardware.
        """)
        st.subheader("Your PDFs")

        uploaded_files = st.file_uploader(
            "Upload your PDFs here", accept_multiple_files=True, type="pdf"
        )
        if uploaded_files:
            st.markdown("#### Uploaded files:")
            for file in uploaded_files:
                st.write(f"- {file.name}")

        if st.button("Process"):
            if not uploaded_files:
                st.warning("Please upload at least one PDF before processing.")
            else:
                with st.spinner("Processing..."):
                    # Reset chat state
                    st.session_state.chat_history = []
                    st.session_state.referenced_pages = []
                    st.session_state.jira_feedback = {}
                    if 'active_jira_request' in st.session_state:
                        del st.session_state.active_jira_request

                    chunks = get_pdf_chunks(uploaded_files)
                    if not chunks:
                        st.error("No readable text found in the PDFs. Please try different files.")
                    else:
                        vectorstore = get_vectorstore(chunks, openai_api_key)
                        if vectorstore:
                            st.session_state.conversation = get_conversation_chain(
                                vectorstore, openai_api_key
                            )
                            if st.session_state.conversation:
                                st.success("Processing complete! You can now ask questions.")

if __name__ == "__main__":
    main()
