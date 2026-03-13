"""NeoStats Research Assistant Chatbot (Streamlit).

Main UI entrypoint. All routing lives in this file.
"""

from __future__ import annotations

import os
import tempfile
import sys
from typing import Any, Dict, List, Optional

import streamlit as st

from config.config import GOOGLE_API_KEY, GROQ_API_KEY, OPENAI_API_KEY
from models.embeddings import get_huggingface_embeddings
from models.llm import get_chatgroq_model, get_gemini_model, get_openai_model
from utils.rag_utils import build_vector_store, load_and_split_documents, retrieve_context
from utils.search_utils import web_search


def _mask_key(key: str) -> str:
    """Mask an API key for safe UI display."""
    k = (key or "").strip()
    if not k:
        return "(missing)"
    if len(k) <= 8:
        return "***"
    return f"{k[:4]}...{k[-4:]}"


def _response_mode_instruction(mode: str) -> str:
    """Return the response style instruction for the selected mode."""
    if mode == "Concise":
        return "Respond in 2-3 sentences maximum. Be direct and to the point."
    return "Provide a thorough, well-structured response with examples where helpful."


def _provider_key_missing(provider: str) -> bool:
    """Check whether the selected provider is missing its required API key."""
    if provider == "Groq":
        return not bool(GROQ_API_KEY)
    if provider == "OpenAI":
        return not bool(OPENAI_API_KEY)
    if provider == "Gemini":
        return not bool(GOOGLE_API_KEY)
    return True


def _get_llm(provider: str):
    """Initialize the selected LLM provider.

    Args:
        provider: One of "Groq", "OpenAI", or "Gemini".

    Returns:
        A LangChain chat model instance.

    Raises:
        RuntimeError: If initialization fails.
    """
    if provider == "Groq":
        return get_chatgroq_model()
    if provider == "OpenAI":
        return get_openai_model()
    if provider == "Gemini":
        return get_gemini_model()
    raise RuntimeError(f"Unknown provider: {provider}")


def _ensure_session_state() -> None:
    """Initialize required Streamlit session state keys."""
    if "messages" not in st.session_state:
        st.session_state.messages = []  # type: ignore[attr-defined]
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None  # type: ignore[attr-defined]
    if "rag_ready" not in st.session_state:
        st.session_state.rag_ready = False  # type: ignore[attr-defined]


def _render_messages(messages: List[Dict[str, str]]) -> None:
    """Render chat history in the Streamlit UI."""
    for msg in messages:
        role = msg.get("role", "assistant")
        content = msg.get("content", "")
        with st.chat_message(role):
            st.markdown(content)


def _build_system_prompt(response_mode: str, optional_context: str) -> str:
    """Build the system prompt template with optional context prepended."""
    mode_instr = _response_mode_instruction(response_mode)
    base = f"You are a helpful research assistant. {mode_instr}\n\n"
    if optional_context.strip():
        base += "Use the following context to answer the user's question:\n\n"
        base += optional_context.strip() + "\n\n"
    return base.strip()


def _messages_to_langchain(messages: List[Dict[str, str]], system_prompt: str) -> List[Any]:
    """Convert session messages into LangChain message objects, prepending system."""
    try:
        from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

        lc: List[Any] = [SystemMessage(content=system_prompt)]
        for m in messages:
            role = m.get("role")
            content = m.get("content", "")
            if role == "user":
                lc.append(HumanMessage(content=content))
            elif role == "assistant":
                lc.append(AIMessage(content=content))
        return lc
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Failed to build chat history for LLM call: {exc}") from exc


def _index_uploaded_files(uploaded_files: list) -> None:
    """Index uploaded PDF/TXT files into a FAISS vector store (once per upload)."""
    try:
        if not uploaded_files:
            return

        with st.spinner("Indexing documents..."):
            temp_paths: list[str] = []
            for f in uploaded_files:
                suffix = os.path.splitext(f.name)[1].lower()
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(f.getvalue())
                    temp_paths.append(tmp.name)

            documents = load_and_split_documents(temp_paths)
            embeddings = get_huggingface_embeddings()
            st.session_state.vector_store = build_vector_store(documents, embeddings)  # type: ignore[attr-defined]
            st.session_state.rag_ready = True  # type: ignore[attr-defined]

        st.sidebar.success("Documents indexed!")
    except Exception as exc:  # noqa: BLE001
        st.session_state.rag_ready = False  # type: ignore[attr-defined]
        st.session_state.vector_store = None  # type: ignore[attr-defined]
        st.sidebar.error(f"Failed to index documents: {exc}")


def chat_page() -> None:
    """Render the chat page UI and handle the full chat flow."""
    _ensure_session_state()

    st.title("NeoStats Research Assistant")
    st.caption("Ask questions grounded in your documents and/or the live web.")

    # Sidebar controls (in required order).
    nav = st.sidebar.radio("Navigation", ["Chat", "Instructions"])
    st.sidebar.divider()
    provider = st.sidebar.selectbox("LLM Provider", ["Groq", "OpenAI", "Gemini"])
    response_mode = st.sidebar.radio("Response mode", ["Concise", "Detailed"])
    rag_enabled = st.sidebar.checkbox("Enable document Q&A (RAG)")
    web_enabled = st.sidebar.checkbox("Enable live web search")

    with st.sidebar.expander("API key status", expanded=False):
        st.caption(f"GROQ_API_KEY: `{_mask_key(GROQ_API_KEY)}`")
        st.caption(f"OPENAI_API_KEY: `{_mask_key(OPENAI_API_KEY)}`")
        st.caption(f"GOOGLE_API_KEY: `{_mask_key(GOOGLE_API_KEY)}`")

    with st.sidebar.expander("Runtime diagnostics", expanded=False):
        try:
            import pydantic
            import langchain_core

            st.caption(f"Python: `{sys.version.split()[0]}`")
            st.caption(f"Executable: `{sys.executable}`")
            st.caption(f"pydantic: `{getattr(pydantic, '__version__', 'unknown')}`")
            st.caption(f"langchain_core: `{getattr(langchain_core, '__version__', 'unknown')}`")
        except Exception as exc:  # noqa: BLE001
            st.caption(f"Diagnostics unavailable: {exc}")

    uploaded_files = None
    if rag_enabled:
        uploaded_files = st.sidebar.file_uploader(
            "Upload documents",
            accept_multiple_files=True,
            type=["pdf", "txt"],
        )

    if st.sidebar.button("Clear chat"):
        st.session_state.messages = []  # type: ignore[attr-defined]

    # Router: if user selected Instructions while on chat page, show it.
    if nav == "Instructions":
        instructions_page()
        return

    # RAG indexing: build once, guarded by rag_ready.
    if rag_enabled and uploaded_files and not st.session_state.rag_ready:  # type: ignore[attr-defined]
        _index_uploaded_files(uploaded_files)

    _render_messages(st.session_state.messages)  # type: ignore[attr-defined]

    user_text: Optional[str] = st.chat_input("Ask a question...")
    if user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})  # type: ignore[attr-defined]
        with st.chat_message("user"):
            st.markdown(user_text)

        if _provider_key_missing(provider):
            st.error(
                f"{provider} API key is missing. Set the appropriate env var in your shell and restart the app."
            )
            return

        # Build optional context.
        context_parts: list[str] = []

        if rag_enabled and st.session_state.rag_ready and st.session_state.vector_store:  # type: ignore[attr-defined]
            try:
                ctx = retrieve_context(user_text, st.session_state.vector_store, k=4)  # type: ignore[attr-defined]
                if ctx.strip():
                    context_parts.append(f"### Document context\n\n{ctx}")
            except Exception as exc:  # noqa: BLE001
                st.error(f"RAG retrieval failed: {exc}")

        if web_enabled:
            try:
                web_ctx = web_search(user_text, num_results=3)
                if web_ctx.strip():
                    context_parts.append(f"### Web search results\n\n{web_ctx}")
            except Exception as exc:  # noqa: BLE001
                st.error(f"Web search failed: {exc}")

        optional_context_block = "\n\n".join(context_parts).strip()
        system_prompt = _build_system_prompt(response_mode, optional_context_block)

        try:
            llm = _get_llm(provider)
            lc_messages = _messages_to_langchain(st.session_state.messages, system_prompt)  # type: ignore[attr-defined]
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    resp = llm.invoke(lc_messages)
                    text = getattr(resp, "content", str(resp))
                    st.markdown(text)
            st.session_state.messages.append({"role": "assistant", "content": text})  # type: ignore[attr-defined]
        except Exception as exc:  # noqa: BLE001
            st.error(f"LLM call failed: {exc}")


def instructions_page() -> None:
    """Render the Instructions page."""
    st.title("Instructions")

    st.subheader("Installation")
    st.markdown(
        """
1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```
3. Run the app:

```bash
streamlit run app.py
```

If you use **uv**, run inside the uv-managed environment:

```bash
uv sync
uv run streamlit run app.py
```
"""
    )

    st.subheader("API Key Setup")
    st.markdown(
        """
Set one or more of these environment variables (then restart Streamlit):

- **Groq**: `GROQ_API_KEY`
- **OpenAI**: `OPENAI_API_KEY`
- **Gemini**: `GOOGLE_API_KEY`
- **Web search (Tavily)**: `TAVILY_API_KEY`

Optional:
- `DEFAULT_GROQ_MODEL`, `DEFAULT_OPENAI_MODEL`, `DEFAULT_GEMINI_MODEL`
- `CHUNK_SIZE`, `CHUNK_OVERLAP`
"""
    )

    st.subheader("Available Models")
    st.markdown(
        """
Defaults can be changed via environment variables:
- Groq: `DEFAULT_GROQ_MODEL` (default: `llama-3.1-8b-instant`)
- OpenAI: `DEFAULT_OPENAI_MODEL` (default: `gpt-4o-mini`)
- Gemini: `DEFAULT_GEMINI_MODEL` (default: `gemini-1.5-flash`)
"""
    )

    st.subheader("How to Use")
    st.markdown(
        """
- Choose **LLM Provider** and **Response mode** in the sidebar.
- Toggle **Enable document Q&A (RAG)** and upload PDF/TXT files to ground answers.
- Toggle **Enable live web search** to supplement answers with fresh information.
- Ask questions in the chat input.
"""
    )

    st.subheader("Tips")
    st.markdown(
        """
- For best RAG results, ask specific questions and include key terms from your documents.
- Use **Detailed** mode for multi-part questions or when you want examples.
"""
    )

    st.subheader("Troubleshooting")
    st.markdown(
        """
- **“API key is missing”**: export the corresponding env var and restart Streamlit.
- **PDF parsing errors**: try re-exporting the PDF or using TXT.
- **Slow indexing**: reduce `CHUNK_SIZE` or upload fewer/shorter documents.
- **ForwardRef/_evaluate errors on Python 3.12**: upgrade Pydantic:

```bash
pip install -U "pydantic>=2.7,<3" "typing-extensions>=4.12"
```
"""
    )


def main() -> None:
    """App entrypoint with simple routing."""
    # Routing is handled inside `chat_page()` to keep the sidebar controls
    # in the exact required order and avoid duplicate sidebar widgets.
    chat_page()


if __name__ == "__main__":
    main()


