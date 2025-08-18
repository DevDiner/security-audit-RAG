#rag_pipeline.py

import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, RetrievalQA
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.llms.base import LLM
from huggingface_hub import InferenceClient
from typing import Optional, List
from pydantic import PrivateAttr

load_dotenv()

CHROMA_PATH = "vectorstore"

# Step 1: Build vector store
def build_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    return vectorstore

# Step 2: Custom Hugging Face LLM wrapper for Flan-T5
class CustomHuggingFaceLLM(LLM):
    model_id: str
    token: str
    max_new_tokens: int = 256
    temperature: float = 0.3

    _client: InferenceClient = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = InferenceClient(model=kwargs["model_id"], token=kwargs["token"])

    @property
    def _llm_type(self) -> str:
        return "custom_huggingface"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        try:
            result = self._client.text_generation(
                prompt=prompt,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature
            )
            return result.strip()

        except Exception as e:
            return f"[Error: {str(e)}]"

# Step 3: Build the full RAG pipeline
def create_rag_chain():
    hf_token = os.getenv("GEMNI_API_KEY")

    llm = CustomHuggingFaceLLM(
        model_id="google/flan-t5-base",  # Free and lightweight
        token=hf_token,
        max_new_tokens=256,
        temperature=0.3
    )

    # T5-style prompt (instruction at the top, followed by context and question)
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "Instruction: You are a Solidity smart contract security auditor. "
            "Answer the QUESTION using only the CONTEXT provided. "
            "Be precise, technical, and do not hallucinate.\n\n"
            "CONTEXT:\n{context}\n\n"
            "QUESTION:\n{question}\n\n"
            "Answer in markdown:"
        )
    )

    llm_chain = LLMChain(llm=llm, prompt=prompt)

    document_chain = StuffDocumentsChain(
        llm_chain=llm_chain,
        document_variable_name="context"
    )

    retriever = build_vectorstore().as_retriever(search_kwargs={"k": 2})

    qa_chain = RetrievalQA(
        retriever=retriever,
        combine_documents_chain=document_chain,
        return_source_documents=True
    )

    return qa_chain
