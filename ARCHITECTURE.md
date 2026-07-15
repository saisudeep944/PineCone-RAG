# Enterprise RAG Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER BROWSER                                │
│                 http://localhost:8501                           │
└────────────────────────┬──────────────────────────────────────┘
                         │
                         │ HTTPS/WSS (Streaming)
                         │
        ┌────────────────▼──────────────────┐
        │   STREAMLIT FRONTEND              │
        │   (frontend/app.py)               │
        │                                   │
        │  • Chat Interface                 │
        │  • Session Manager                │
        │  • Document Upload                │
        │  • Sources Panel                  │
        │  • Dark Theme UI                  │
        └────────────────┬──────────────────┘
                         │
                         │ REST API + NDJSON
                         │ http://localhost:8000
                         │
        ┌────────────────▼──────────────────────────────────┐
        │       FASTAPI BACKEND                             │
        │       (app/api/main.py)                           │
        │                                                   │
        │  Endpoints:                                       │
        │  • POST /chat/stream (NDJSON)                    │
        │  • POST /session/create                          │
        │  • GET /sessions                                 │
        │  • GET /namespaces                               │
        │  • POST /upload                                  │
        └────────────┬──────────────────────┬──────────────┘
                     │                      │
        ┌────────────▼──────────┐    ┌─────▼──────────────┐
        │  LLM SERVICE          │    │ RAG SERVICES       │
        │  (app/services/llm/)  │    │ (app/services/)    │
        │                       │    │                    │
        │ • Groq LLM API        │    │ • Retrieval        │
        │ • Prompt Building     │    │ • Reranking        │
        │ • Response Streaming  │    │ • Hybrid Search    │
        │ • Intent Classifier   │    │ • Embeddings       │
        │ • Query Rewriter      │    │ • Document Parsing │
        │ • Conversation        │    │ • BM25 Search      │
        │                       │    │ • Session Mgmt     │
        └───────────┬───────────┘    └────────┬───────────┘
                    │                         │
        ┌───────────▼─────────────────────────▼───────────┐
        │        EXTERNAL SERVICES & STORAGE              │
        │                                                  │
        │  ┌──────────────────┐  ┌──────────────────┐    │
        │  │  PINECONE        │  │  GROQ LLM        │    │
        │  │  Vector DB       │  │  llama-3.3-70b   │    │
        │  │  - Embeddings    │  │  or llama-3.1-8b │    │
        │  │  - Similarity    │  │  - Token Gen      │    │
        │  │  - Metadata      │  │  - Context        │    │
        │  └──────────────────┘  └──────────────────┘    │
        │                                                  │
        │  ┌──────────────────┐  ┌──────────────────┐    │
        │  │  REDIS           │  │  LOCAL STORAGE   │    │
        │  │  Session Cache   │  │  - Uploaded Docs │    │
        │  │  - Messages      │  │  - Parsed Files  │    │
        │  │  - Context       │  │  - Session Data  │    │
        │  └──────────────────┘  └──────────────────┘    │
        │                                                  │
        └──────────────────────────────────────────────────┘
```

## Data Flow: User Query → Response

```
USER INPUT
    │
    ▼
STREAMLIT APP
    │
    ├─ Display user message
    │
    ├─ POST /chat/stream with session_id + message
    │
    ▼
FASTAPI BACKEND
    │
    ├─ Verify session exists
    │
    ├─ Process message:
    │   ├─ Intent Classification (RAG vs Conversational)
    │   ├─ Query Rewriting (if needed)
    │   ├─ Retrieve from Pinecone
    │   │   ├─ Generate embeddings
    │   │   ├─ Semantic search (cosine similarity)
    │   │   ├─ BM25 hybrid search
    │   │   ├─ Reranking
    │   │
    │   └─ Generate response via Groq LLM
    │       ├─ Prompt building with context
    │       ├─ Token generation
    │       ├─ Format with headers/sections
    │
    ├─ Stream response back as NDJSON:
    │   ├─ {"type": "token", "content": "word"}
    │   ├─ {"type": "token", "content": " "}
    │   ├─ ...
    │   ├─ {"type": "metadata", "sources": [...]}
    │   ├─ {"type": "complete"}
    │
    ▼
STREAMLIT FRONTEND
    │
    ├─ Parse NDJSON events
    │
    ├─ Accumulate tokens: "word " + "word " + "word"
    │
    ├─ Re-render with updated text
    │
    ├─ On metadata: Extract sources
    │
    ├─ Display complete response
    │
    ├─ Show sources panel (expandable)
    │
    ├─ Save to session state
    │
    ▼
DISPLAY TO USER
```

## Directory Structure: Complete

```
Pinecone_RAG/
│
├── main.py                           ← START BACKEND
├── requirements.txt                  ← Python deps
├── README.md                         ← Project docs
│
├── frontend/                         ← STREAMLIT APP (NEW)
│   ├── app.py                       ◄─ START HERE (Main chat)
│   │
│   ├── pages/
│   │   ├── upload.py                 (Document upload)
│   │   ├── sessions.py               (Session manager)
│   │   └── chat.py                   (Integrated note)
│   │
│   ├── services/
│   │   └── api_client.py             (Backend API calls)
│   │
│   ├── utils/
│   │   └── session_state.py          (State management)
│   │
│   ├── styles/
│   │   └── custom.css                (Dark theme)
│   │
│   ├── .streamlit/
│   │   └── config.toml               (Streamlit config)
│   │
│   ├── requirements.txt              (Streamlit deps)
│   ├── README.md                     (Frontend docs)
│   └── __pycache__/
│
├── app/                              ← BACKEND (Python)
│   ├── api/
│   │   ├── main.py                   (FastAPI routes)
│   │   └── schemas.py
│   │
│   ├── core/
│   │   ├── chat_engine.py            (Chat orchestration)
│   │   ├── config.py
│   │   ├── namespace_service.py
│   │   └── pinecone_client.py
│   │
│   ├── services/
│   │   ├── embedding_service.py
│   │   ├── ingestion_service.py
│   │   ├── pinecone_service.py
│   │   ├── retrieval_service.py
│   │   │
│   │   ├── evaluation/
│   │   │   ├── retrieval_metrics.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── hybrid/
│   │   │   ├── bm25_service.py
│   │   │   ├── fusion_service.py
│   │   │   ├── reranker_service.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── llm/
│   │   │   ├── conversation_service.py
│   │   │   ├── guardrails.py
│   │   │   ├── intent_classifier.py
│   │   │   ├── llm_service.py
│   │   │   ├── prompt_builder.py
│   │   │   ├── query_rewriter.py
│   │   │   ├── response_formatter.py
│   │   │   ├── rewrite_classifier.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── loaders/
│   │   │   ├── csv_loader.py
│   │   │   ├── document_router.py
│   │   │   ├── docx_loader.py
│   │   │   ├── pdf_loader.py
│   │   │   ├── txt_loader.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── memory/
│   │   │   ├── redis_memory.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── observability/
│   │   │   ├── trace_service.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── session/
│   │   │   └── session_manager.py
│   │   │
│   │   ├── upload/
│   │   │   └── upload_service.py
│   │   │
│   │   └── __init__.py
│   │
│   ├── utils/
│   └── chat_app.py
│
├── data/
│   └── american_airlines_dataset.csv
│
├── evaluation_data/
│   └── benchmark_queries.py
│
├── tests/
│   ├── test_*.py                    (Various test files)
│   └── zFinal_Evaluator_AvgMRR.py
│
├── uploaded_docs/                   (Document storage)
│
├── STREAMLIT_QUICKSTART.md          ◄─ READ THIS FIRST!
├── FRONTEND_INTEGRATION.md          (This guide)
├── DEPLOYMENT.md                    (Production guide)
└── .gitignore
```

## Component Interactions

```
Streamlit Frontend          FastAPI Backend         External Services
└─ app.py                   └─ api/main.py          └─ Pinecone, Groq, Redis
   ├─ Chat UI              │   ├─ Routes
   ├─ Streaming Parser     │   │   ├─ /chat/stream   ◄─ stream_chat()
   ├─ Session Mgmt         │   │   ├─ /upload
   ├─ Upload UI            │   │   └─ /namespaces
   │                       │   │
   └─ api_client.py        │   ├─ chat_engine.py
      (HTTP Calls)         │   │   ├─ process_chat_message()
                           │   │   └─ stream_structured_response()
                           │   │
                           │   ├─ retrieval_service.py
                           │   │   └─ retrieve_context()
                           │   │
                           │   ├─ llm_service.py
                           │   │   └─ generate_response()
                           │   │
                           │   └─ session_manager.py
                           │       └─ create/load sessions
                           │
                           └─ Pinecone Vector DB
                               Redis Cache
```

## Message Flow: Single Chat Query

```
┌──────────────────────────────────────────────────────────────────┐
│                        COMPLETE FLOW                             │
└──────────────────────────────────────────────────────────────────┘

1. USER TYPES MESSAGE
   ├─ "Tell me about advanced flight systems"
   └─ Streamlit captures input

2. STREAMLIT SENDS REQUEST
   ├─ POST /chat/stream
   ├─ Body: {
   │    "session_id": "abc123...",
   │    "message": "Tell me about..."
   │ }
   └─ Sets up response streaming

3. BACKEND RECEIVES REQUEST
   ├─ Validates session_id
   ├─ Stores message in session
   └─ Begins processing

4. INTENT CLASSIFICATION
   ├─ Analyzes user query
   ├─ Determines: RAG query
   └─ Routes to retrieval

5. QUERY REWRITING (Optional)
   ├─ Improves query clarity
   ├─ Expands search terms
   └─ "Tell me about..." → "What are advanced flight control systems?"

6. DOCUMENT RETRIEVAL
   ├─ Embedding Service
   │  └─ Converts query to vector: [0.2, -0.4, 0.8, ...]
   │
   ├─ Semantic Search (Pinecone)
   │  └─ Finds similar chunks (cosine similarity)
   │     [chunk_1: 0.89, chunk_2: 0.87, chunk_3: 0.82, ...]
   │
   ├─ BM25 Hybrid Search
   │  └─ Keyword matching: [chunk_1: score, chunk_5: score, ...]
   │
   ├─ Score Fusion
   │  └─ Combines both signals: [chunk_1: 0.92, chunk_2: 0.88, ...]
   │
   └─ Reranking
      └─ Fine-grained relevance: [chunk_1: 0.95, chunk_2: 0.89, ...]

7. PROMPT BUILDING
   ├─ System: "You are an expert..."
   ├─ Context: "[Retrieved chunk 1] [Retrieved chunk 2]..."
   ├─ History: "[Previous exchanges]"
   └─ Query: "Tell me about..."

8. LLM GENERATION (Groq API)
   ├─ Model: llama-3.3-70b or llama-3.1-8b
   ├─ Streaming enabled
   ├─ Token generation: "Advanced" "flight" "systems" "use" ...
   └─ Returns stream of tokens

9. RESPONSE FORMATTING
   ├─ Preserves whitespace with regex
   ├─ Adds markdown headers/sections
   ├─ Collects tokens: ["Advanced", " ", "flight", ...]
   └─ Yields as NDJSON events

10. STREAMING RESPONSE
    ├─ Event 1: {"type": "token", "content": "Advanced"}
    ├─ Event 2: {"type": "token", "content": " "}
    ├─ Event 3: {"type": "token", "content": "flight"}
    ├─ Event N: {"type": "token", "content": "..."}
    ├─ Event M: {"type": "metadata", "sources": [...]}
    └─ Event L: {"type": "complete"}

11. FRONTEND RECEIVES STREAM
    ├─ Parses each NDJSON line
    ├─ Extracts token content
    ├─ Accumulates: "Advanced flight..."
    ├─ Re-renders in real-time
    └─ User sees typing animation

12. METADATA RECEIVED
    ├─ Extracts source documents
    ├─ Stores: [{file_name, chunk_index, rerank_score, text}, ...]
    ├─ Makes "📚 View Sources" expandable
    └─ Prepares for display

13. STREAM COMPLETE
    ├─ Message saved to session_state
    ├─ Sources stored with message
    ├─ Session synced with backend
    └─ Ready for next query

14. USER SEES FINAL RESULT
    ├─ Complete response displayed
    ├─ "📚 View Sources" expanded
    ├─ Shows source cards with:
    │   ├─ 📄 document.pdf
    │   ├─ Chunk #5 • Score: 0.95
    │   └─ Preview text...
    └─ Ready for follow-up question

15. CYCLE REPEATS
    └─ User can ask follow-up, upload docs, or switch sessions
```

---

**Architecture Complete!** 🏗️
