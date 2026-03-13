# NeoStats Research Assistant (Streamlit)

A production-ready **research assistant chatbot** that answers questions using:

- **Your uploaded documents (RAG)**: PDF/TXT → chunking → embeddings → FAISS retrieval
- **Live web search (Tavily)**: optional, toggleable
- **Multiple LLM providers**: Groq, OpenAI, Gemini (selectable in the UI)
- **Response modes**: Concise vs Detailed (injects style instructions into the system prompt)

This project follows the required modular structure from the NeoStats AI Engineer case study and keeps secrets out of source control.

## Demo (RAG + Tavily)

<<<<<<< HEAD
Live app: `https://neostats-research-assistant.streamlit.app/`

=======
>>>>>>> dad6f2a (added readme file with output ss)
Save the screenshot you shared as `demo.png` and GitHub will render it here:

![NeoStats Research Assistant — RAG + Tavily demo](assets/demo.png)

## Features

- **LLM provider switching**: Groq / OpenAI / Gemini
- **RAG indexing (cached)**:
  - Upload PDF/TXT files
  - Index once per upload (cached in `st.session_state`)
  - Retrieve top-k chunks to ground answers
- **Web search tool**:
  - Uses Tavily when enabled
  - Fails gracefully (empty results) if key is missing
- **Safety & quality**:
  - No API keys hardcoded
  - External calls wrapped in `try/except`
  - UI surfaces errors with `st.error(...)`

## Project Structure

```
project/
├── config/
│   └── config.py
├── models/
│   ├── llm.py
│   └── embeddings.py
├── utils/
│   ├── rag_utils.py
│   └── search_utils.py
├── app.py
└── requirements.txt
```

## Requirements

- Python **3.12+**
- One LLM API key (Groq/OpenAI/Gemini)
- Optional: Tavily API key for live web search

## Installation

### Option A: `uv` (recommended)

```bash
uv sync
uv run streamlit run app.py
```

### Option B: `pip`

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Configuration (Secrets)

### Local development with `.env`

Create a `.env` file in the project root (this repo ignores it via `.gitignore`):

```env
GROQ_API_KEY=...
TAVILY_API_KEY=...
```

Supported variables:

- **LLM keys**
  - `GROQ_API_KEY`
  - `OPENAI_API_KEY`
  - `GOOGLE_API_KEY`
- **Search key**
  - `TAVILY_API_KEY`
- **Optional defaults**
  - `DEFAULT_GROQ_MODEL` (default: `llama-3.1-8b-instant`)
  - `DEFAULT_OPENAI_MODEL` (default: `gpt-4o-mini`)
  - `DEFAULT_GEMINI_MODEL` (default: `gemini-1.5-flash`)
- **RAG chunking**
  - `CHUNK_SIZE` (default: `500`)
  - `CHUNK_OVERLAP` (default: `50`)

### Streamlit Community Cloud (recommended for deployment)

In Streamlit Cloud → **App settings → Secrets**, paste TOML:

```toml
GROQ_API_KEY = "..."
TAVILY_API_KEY = "..."
```

> Don’t commit `.env` to GitHub. Use Streamlit secrets for deployment.

## Usage

1. Start the app.
2. In the sidebar:
   - Choose **LLM Provider**
   - Choose **Response mode**
   - Enable **document Q&A (RAG)** and upload PDF/TXT files (optional)
   - Enable **live web search** (optional)
3. Ask questions in the chat input.

## Troubleshooting

- **API key missing**: ensure the variable is present in `.env` (local) or Streamlit Secrets (cloud), then restart the app.
- **RAG indexing errors**: confirm you’re running via `uv run ...` (consistent environment) and that PDFs are readable (try TXT if needed).
- **Web search shows nothing**: set `TAVILY_API_KEY` or disable web search.

## License

Internal / assignment use.



