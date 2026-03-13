"""LLM provider wrappers for the NeoStats chatbot.

This module centralizes initialization of supported chat models to keep `app.py`
clean and to ensure consistent error handling across providers.
"""

from __future__ import annotations

from typing import Optional

from config.config import (
    DEFAULT_GEMINI_MODEL,
    DEFAULT_GROQ_MODEL,
    DEFAULT_OPENAI_MODEL,
    GOOGLE_API_KEY,
    GROQ_API_KEY,
    OPENAI_API_KEY,
)


def get_chatgroq_model(model_name: Optional[str] = None):
    """Create and return a Groq chat model.

    Args:
        model_name: Optional override for the Groq model name.

    Returns:
        An initialized `langchain_groq.ChatGroq` instance.

    Raises:
        RuntimeError: If initialization fails for any reason.
    """
    try:
        from langchain_groq import ChatGroq

        name = model_name or DEFAULT_GROQ_MODEL
        return ChatGroq(api_key=GROQ_API_KEY, model=name)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Failed to initialize Groq chat model: {exc}") from exc


def get_openai_model(model_name: Optional[str] = None):
    """Create and return an OpenAI chat model.

    Args:
        model_name: Optional override for the OpenAI model name.

    Returns:
        An initialized `langchain_openai.ChatOpenAI` instance.

    Raises:
        RuntimeError: If initialization fails for any reason.
    """
    try:
        from langchain_openai import ChatOpenAI

        name = model_name or DEFAULT_OPENAI_MODEL
        return ChatOpenAI(api_key=OPENAI_API_KEY, model=name)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Failed to initialize OpenAI chat model: {exc}") from exc


def get_gemini_model(model_name: Optional[str] = None):
    """Create and return a Gemini chat model.

    Args:
        model_name: Optional override for the Gemini model name.

    Returns:
        An initialized `langchain_google_genai.ChatGoogleGenerativeAI` instance.

    Raises:
        RuntimeError: If initialization fails for any reason.
    """
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI

        name = model_name or DEFAULT_GEMINI_MODEL
        return ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model=name)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Failed to initialize Gemini chat model: {exc}") from exc


