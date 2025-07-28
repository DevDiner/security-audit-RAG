from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFaceHub
from langchain.chains import RetrievalQA
from langchain.callbacks.base import BaseCallbackHandler
from langchain.docstore.document import Document

CHROMA_PATH = "vectorstore"

def build_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    return vectorstore

def create_rag_chain():
    vectorstore = build_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    llm = HuggingFaceHub(
        repo_id="tiiuae/falcon-7b-instruct",  # Free inference model
        model_kwargs={"temperature": 0.2, "max_new_tokens": 256}
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True  # ✅ Ensure we get retrieved docs
    )
    return qa_chain
