# qa_bot.py

from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain

from config import OPENAI_API_KEY

# initialize once
_embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
_vectordb   = Chroma(persist_directory="db", embedding_function=_embeddings)
_retriever  = _vectordb.as_retriever(search_kwargs={"k": 5})
_llm        = ChatOpenAI(temperature=0.0, openai_api_key=OPENAI_API_KEY)

_chain = ConversationalRetrievalChain.from_llm(
    llm=_llm,
    retriever=_retriever,
    return_source_documents=True
)

def answer_question(question: str, chat_history: list[tuple[str,str]] = None):
    """
    Returns a dict with:
      - 'answer': the generated answer (with citations)
      - 'source_documents': list of metadata for cited chunks
      - 'chat_history': updated list of (q,a)
    """
    if chat_history is None:
        chat_history = []
    result = _chain({"question": question, "chat_history": chat_history})
    return {
        "answer": result["answer"],
        "source_documents": result["source_documents"],
        "chat_history": result["chat_history"]
    }
