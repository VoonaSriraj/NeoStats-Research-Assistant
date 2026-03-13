# NeoStats Research Assistant (Streamlit)

A production-ready **AI research assistant chatbot** that answers questions using:

* 📄 **Your uploaded documents (RAG)** – PDF/TXT → chunking → embeddings → FAISS retrieval
* 🌐 **Live web search** using Tavily
* 🤖 **Multiple LLM providers** – Groq, OpenAI, Gemini
* ⚡ **Fast UI** built with Streamlit

The assistant combines **Retrieval Augmented Generation (RAG)** with **live search** to generate grounded and up-to-date answers.

---

# 🚀 Live Demo

🔗 **Try the app:**
https://neostats-research-assistant.streamlit.app/

Click the screenshot below to open the demo.

[![NeoStats Research Assistant Demo](assets/demo.png)](https://neostats-research-assistant.streamlit.app/)

---

# ✨ Features

### 🔹 Retrieval Augmented Generation (RAG)

* Upload **PDF or TXT files**
* Automatic **chunking**
* Vector embeddings
* **FAISS similarity search**
* Context-aware responses

### 🔹 Live Web Search

* Uses **Tavily API**
* Toggleable in UI
* Retrieves recent information from the web

### 🔹 Multiple LLM Providers

Switch between:

* **Groq**
* **OpenAI**
* **Google Gemini**

Directly from the sidebar.

### 🔹 Response Modes

Two output styles:

* **Concise** → short answers
* **Detailed** → in-depth explanations

---

# 🧠 System Architecture

```
User Query
    │
    ▼
Streamlit Chat UI
    │
    ▼
Query Router
 ├── Document Retrieval (FAISS)
 │      │
 │      ▼
 │   Context Chunks
 │
 └── Tavily Web Search
        │
        ▼
    Search Results
        │
        ▼
      LLM
 (Groq / OpenAI / Gemini)
        │
        ▼
   Generated Response
```

---

# 📁 Project Structure

```
project/
│
├── config/
│   └── config.py
│
├── models/
│   ├── llm.py
│   └── embeddings.py
│
├── utils/
│   ├── rag_utils.py
│   └── search_utils.py
│
├── assets/
│   └── demo.png
│
├── app.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Requirements

* Python **3.12+**
* One LLM API key (Groq/OpenAI/Gemini)
* Optional **Tavily API key** for web search

---

# 🛠 Installation

## Option 1 — Using pip

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Option 2 — Using uv (recommended)

```bash
uv sync
uv run streamlit run app.py
```

---

# 🔑 Configuration

Create a `.env` file:

```
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key
OPENAI_API_KEY=your_key
GOOGLE_API_KEY=your_key
```

Optional settings:

```
DEFAULT_GROQ_MODEL=llama-3.1-8b-instant
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

⚠️ Do **not commit `.env` to GitHub**.

---

# 🧪 Usage

1️⃣ Run the app

```
streamlit run app.py
```

2️⃣ In the sidebar:

* Select **LLM provider**
* Choose **response mode**
* Upload documents for **RAG**
* Enable **web search**

3️⃣ Ask questions in the chat.

---

# 🛡 Safety & Error Handling

* API keys stored in **environment variables**
* External calls wrapped in **try/except**
* Errors surfaced using **Streamlit UI alerts**

---

# 📌 Technologies Used

* **Streamlit**
* **LangChain style RAG pipeline**
* **FAISS**
* **Sentence Transformers**
* **Groq / OpenAI / Gemini APIs**
* **Tavily Web Search**

---

# 📄 License

Internal / Assignment Use
