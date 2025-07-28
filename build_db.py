import os
import requests
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

CHROMA_PATH = "vectorstore"
DOCS_PATH = "docs"

OPENZEPPELIN_URLS = {
    "openzeppelin-access-control.md": "https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/v4.9.3/contracts/access/Ownable.sol",
    "openzeppelin-upgradeable.md": "https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts-upgradeable/v4.9.3/contracts/proxy/utils/UUPSUpgradeable.sol",
    "openzeppelin-security.md": "https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/v4.9.3/contracts/security/ReentrancyGuard.sol",
    "openzeppelin-delegatecall.md": "https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/v4.9.3/contracts/proxy/Proxy.sol",
    "openzeppelin-erc20.md": "https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/v4.9.3/contracts/token/ERC20/ERC20.sol",
    "openzeppelin-erc721.md": "https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/v4.9.3/contracts/token/ERC721/ERC721.sol",
    "openzeppelin-erc1155.md": "https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/v4.9.3/contracts/token/ERC1155/ERC1155.sol"
}

EIP_URLS = {
    "eip-20.md": "https://raw.githubusercontent.com/ethereum/EIPs/master/EIPS/eip-20.md",
    "eip-721.md": "https://raw.githubusercontent.com/ethereum/EIPs/master/EIPS/eip-721.md",
    "eip-1155.md": "https://raw.githubusercontent.com/ethereum/EIPs/master/EIPS/eip-1155.md",
    "eip-196.md": "https://raw.githubusercontent.com/ethereum/EIPs/master/EIPS/eip-196.md",
    "eip-897.md": "https://raw.githubusercontent.com/ethereum/EIPs/master/EIPS/eip-897.md",
    "eip-1822.md": "https://raw.githubusercontent.com/ethereum/EIPs/master/EIPS/eip-1822.md",
    "eip-1967.md": "https://raw.githubusercontent.com/ethereum/EIPs/master/EIPS/eip-1967.md",
    "eip-2535.md": "https://raw.githubusercontent.com/ethereum/EIPs/master/EIPS/eip-2535.md"
}

def download_docs():
    os.makedirs(DOCS_PATH, exist_ok=True)

    for filename, url in OPENZEPPELIN_URLS.items():
        content = requests.get(url).text
        with open(os.path.join(DOCS_PATH, filename), "w", encoding="utf-8") as f:
            f.write(content)

    for filename, url in EIP_URLS.items():
        content = requests.get(url).text
        with open(os.path.join(DOCS_PATH, filename), "w", encoding="utf-8") as f:
            f.write(content)

    print("✅ Docs downloaded successfully!")

def build_vectorstore():
    print("✅ Building vectorstore...")
    docs = []
    for filename in os.listdir(DOCS_PATH):
        with open(os.path.join(DOCS_PATH, filename), "r", encoding="utf-8") as f:
            text = f.read()
            docs.append(text)

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = [Document(page_content=chunk) for text in docs for chunk in splitter.split_text(text)]

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=CHROMA_PATH)
    vectorstore.persist()
    print("✅ Vectorstore built and saved to disk!")

if __name__ == "__main__":
    download_docs()
    build_vectorstore()
