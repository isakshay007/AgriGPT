# backend/core/llm_client.py

"""
OpenAPI-safe LLM Client
-----------------------
No globals, no caching of ChatGroq(), avoids $ref crashes.
"""

from __future__ import annotations
from langchain_groq import ChatGroq
from backend.core.config import settings


def get_llm() -> ChatGroq:
    """
    Always returns a fresh lightweight ChatGroq instance.
    Safe for OpenAPI because no global objects are created.
    """
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.TEXT_MODEL_NAME,
        temperature=0.2,
        max_tokens=1500,
    )
