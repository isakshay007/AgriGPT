# backend/services/rag_service.py

import json
import os
from typing import List, Dict
import unicodedata
import re

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/subsidies.json")
VECTOR_DB_PATH = os.path.join(os.path.dirname(__file__), "../data/faiss_index")


def _clean_query(text: str) -> str:
    """Clean query for FAISS safety."""
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[\x00-\x1f\x7f]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


class RAG:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RAG, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = None

        # Try load FAISS
        if os.path.exists(VECTOR_DB_PATH):
            try:
                print("Loading existing FAISS index...")
                self.vector_store = FAISS.load_local(
                    VECTOR_DB_PATH,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                print("FAISS index loaded.")
                return
            except Exception as e:
                print(f"[RAG] Failed to load FAISS index: {e}")
                print("[RAG] Rebuilding fresh index...")
                try:
                    import shutil
                    if os.path.exists(VECTOR_DB_PATH):
                        shutil.rmtree(VECTOR_DB_PATH)
                except:
                    pass

        # Build new index
        if not os.path.exists(DATA_PATH):
            print(f"[RAG] subsidies.json not found at: {DATA_PATH}")
            return

        with open(DATA_PATH, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        documents = []
        for item in raw_data:
            scheme_name = item.get("scheme_name", "Unknown Scheme")
            eligibility = item.get("eligibility", "Not Provided")
            benefits = item.get("benefits", "Not Provided")
            notes = item.get("notes", "")

            content = (
                f"Scheme: {scheme_name}\n"
                f"Eligibility: {eligibility}\n"
                f"Benefits: {benefits}\n"
                f"Notes: {notes}\n"
            )

            documents.append(
                Document(page_content=content, metadata=item)
            )

        print("[RAG] Building FAISS index...")
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        self.vector_store.save_local(VECTOR_DB_PATH)
        print("[RAG] FAISS index built and saved successfully.")

    def retrieve(self, query: str, k: int = 2) -> List[Dict[str, str]]:
        """
        ✅ SAFE: Returns plain dicts (no Pydantic).
        OpenAPI will never touch this.
        """
        if not query or not query.strip():
            return []

        query_clean = _clean_query(query)

        if not self.vector_store:
            print("[RAG] Vector store not loaded.")
            return []

        try:
            docs = self.vector_store.similarity_search(query_clean, k=k)
        except Exception as e:
            print(f"[RAG] Retrieval error: {e}")
            return []

        results = []
        for d in docs:
            meta = d.metadata or {}
            
            # ✅ Return plain dict (OpenAPI-safe)
            results.append({
                "scheme_name": str(meta.get("scheme_name", "Unknown Scheme")),
                "eligibility": str(meta.get("eligibility", "Not Provided")),
                "benefits": str(meta.get("benefits", "Not Provided")),
                "application_steps": str(meta.get("application_steps", "")),
                "documents": str(meta.get("documents", "")),
                "notes": str(meta.get("notes", "")),
            })

        return results


# Singleton instance
rag_service = RAG()