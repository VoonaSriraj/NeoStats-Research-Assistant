"""RAG utilities: document loading, chunking, vector store build, and retrieval."""

from __future__ import annotations

from typing import List

from config.config import CHUNK_OVERLAP, CHUNK_SIZE


def load_and_split_documents(file_paths: list[str]) -> list:
    """Load PDF/TXT documents from disk and split them into chunks.

    Args:
        file_paths: List of file paths to load. Supported extensions are `.pdf` and `.txt`.

    Returns:
        A list of LangChain `Document` chunks.

    Raises:
        RuntimeError: If loading or splitting fails.
    """
    try:
        try:
            # LangChain 0.2.x
            from langchain.text_splitter import RecursiveCharacterTextSplitter
        except Exception:
            # LangChain 1.x+ moved splitters here.
            from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_community.document_loaders import PyPDFLoader, TextLoader

        docs: List = []
        for path in file_paths:
            lower = path.lower()
            if lower.endswith(".pdf"):
                loader = PyPDFLoader(path)
            elif lower.endswith(".txt"):
                loader = TextLoader(path, encoding="utf-8")
            else:
                raise RuntimeError(f"Unsupported file type for RAG: {path}")

            docs.extend(loader.load())

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )
        return splitter.split_documents(docs)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Failed to load/split documents for RAG: {exc}") from exc


def build_vector_store(documents: list, embeddings):
    """Build an in-memory FAISS vector store from documents.

    Args:
        documents: List of LangChain `Document` chunks.
        embeddings: Embeddings instance compatible with LangChain vector stores.

    Returns:
        An in-memory FAISS vector store.

    Raises:
        RuntimeError: If vector store construction fails.
    """
    try:
        from langchain_community.vectorstores import FAISS

        return FAISS.from_documents(documents, embeddings)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Failed to build FAISS vector store: {exc}") from exc


def retrieve_context(query: str, vector_store, k: int = 4) -> str:
    """Retrieve top-k relevant chunks and return them as a single context string.

    Args:
        query: User query to retrieve context for.
        vector_store: FAISS vector store instance.
        k: Number of chunks to retrieve.

    Returns:
        A single string containing joined chunk contents. Empty string if no results.

    Raises:
        RuntimeError: If retrieval fails.
    """
    try:
        docs = vector_store.similarity_search(query, k=k)
        if not docs:
            return ""
        return "\n\n---\n\n".join([d.page_content for d in docs if getattr(d, "page_content", "")])
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Failed to retrieve RAG context: {exc}") from exc


