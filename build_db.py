from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os

CHROMA_PATH = "vectorstore"
DOCS_PATH = "docs"

def load_docs():
    texts = []
    for filename in os.listdir(DOCS_PATH):
        with open(os.path.join(DOCS_PATH, filename), "r", encoding="utf-8") as f:
            texts.append(f.read())
    return texts

if __name__ == "__main__":
    docs = load_docs()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = [Document(page_content=chunk) for text in docs for chunk in splitter.split_text(text)]

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=CHROMA_PATH)
    vectorstore.persist()
    print("✅ Vectorstore built successfully!")
