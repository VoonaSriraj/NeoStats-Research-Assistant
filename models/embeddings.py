"""Embedding model initialization for RAG."""

from __future__ import annotations


def get_huggingface_embeddings():
    """Create and return a local HuggingFace embedding model.

    Uses a lightweight sentence-transformers model that does not require an API key.

    Returns:
        An initialized embeddings instance compatible with LangChain vector stores.

    Raises:
        RuntimeError: If initialization fails for any reason.
    """
    try:
        # Prefer `langchain_huggingface` when available.
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    except Exception:
        try:
            # Fallback for older environments.
            from langchain_community.embeddings import HuggingFaceEmbeddings

            return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"Failed to initialize HuggingFace embeddings: {exc}") from exc


