"""Configuration constants for the NeoStats Research Assistant Chatbot.

All API keys must be provided via environment variables. This module reads them
once at import time and exposes them as constants for the rest of the app.
"""

from __future__ import annotations

import os

# Load `.env` if present so local development can use environment-style config
# without exporting variables in the shell.
try:
    from dotenv import load_dotenv

    # `override=False` ensures real environment variables take precedence.
    load_dotenv(override=False)
except Exception:
    # If python-dotenv isn't installed, we simply fall back to os.environ.
    pass

# LLM provider API keys (empty string if not set).
GROQ_API_KEY: str = os.environ.get("GROQ_API_KEY", "")
OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
GOOGLE_API_KEY: str = os.environ.get("GOOGLE_API_KEY", "")

# Web search API keys (use one of the below).
SERPAPI_KEY: str = os.environ.get("SERPAPI_KEY", "")
TAVILY_API_KEY: str = os.environ.get("TAVILY_API_KEY", "")

# Default model names (reasonable, commonly available defaults).
DEFAULT_GROQ_MODEL: str = os.environ.get("DEFAULT_GROQ_MODEL", "llama-3.1-8b-instant")
DEFAULT_OPENAI_MODEL: str = os.environ.get("DEFAULT_OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_GEMINI_MODEL: str = os.environ.get("DEFAULT_GEMINI_MODEL", "gemini-1.5-flash")

# RAG chunking defaults.
CHUNK_SIZE: int = int(os.environ.get("CHUNK_SIZE", "500"))
CHUNK_OVERLAP: int = int(os.environ.get("CHUNK_OVERLAP", "50"))


