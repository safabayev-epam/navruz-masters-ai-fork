# utils/vectorstore.py

import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

from constants import STRICT_PROMPT

def get_vectorstore(chunks, api_key):
    texts     = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    try:
        embeddings = OpenAIEmbeddings(openai_api_key=api_key, model="text-embedding-3-small")
        vectorstore = FAISS.from_texts(texts=texts, embedding=embeddings, metadatas=metadatas)
        return vectorstore
    except Exception as e:
        st.error(f"Failed to create vector store: {e}")
        return None

def get_conversation_chain(vectorstore, api_key):
    strict_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=STRICT_PROMPT
    )
    try:
        llm = ChatOpenAI(openai_api_key=api_key, model="gpt-4.1-mini")
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": strict_prompt},
        )
        return conversation_chain
    except Exception as e:
        st.error(f"Failed to create conversation chain: {e}")
        return None
