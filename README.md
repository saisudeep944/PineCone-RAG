# Pinecone RAG

Pinecone RAG is an enterprise-style retrieval-augmented generation (RAG) application that lets users chat with their documents using a FastAPI backend and a Streamlit frontend. The system combines vector search, hybrid retrieval, reranking, and LLM-based response generation to provide grounded answers over uploaded content.

## Features

- Document upload and ingestion for PDF, CSV, TXT, and DOCX files
- Semantic retrieval using Pinecone vector search
- Hybrid search with BM25 and reranking
- Conversational chat with session support
- Streaming responses for a more interactive experience
- Namespace-based organization for multi-project use
- Streamlit-based web interface for chat, uploads, and sessions

## Project Structure

- `main.py` - Starts the backend server
- `app/` - Core backend application
  - `app/api/` - FastAPI routes and schemas
  - `app/core/` - Configuration, chat orchestration, and Pinecone integration
  - `app/services/` - Retrieval, ingestion, LLM, upload, and session services
- `frontend/` - Streamlit frontend application
- `tests/` - Automated test suite
- `data/` and `uploaded_docs/` - Sample data and uploaded documents

## Tech Stack

- Python
- FastAPI
- Streamlit
- Pinecone
- Groq LLM
- Redis (optional for memory/session support)

## Prerequisites

Make sure you have:

- Python 3.10+
- A Pinecone account and index
- A Groq API key

## Environment Variables

Create a `.env` file in the project root with:

```env
PINECONE_API_KEY=your_pinecone_api_key
INDEX_NAME=your_pinecone_index_name
GROQ_API_KEY=your_groq_api_key
```

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

### Start the backend

```bash
python main.py
```

This starts the FastAPI backend on `http://127.0.0.1:8000`.

### Start the frontend

```bash
streamlit run frontend/app.py
```

The frontend will open in your browser at `http://localhost:8501`.

## Usage

1. Upload documents through the Streamlit interface.
2. Select or create a namespace.
3. Start chatting with the uploaded knowledge base.
4. Review retrieved sources and session history.

## Testing

Run the test suite with:

```bash
pytest
```

## Notes

This project is designed for document-grounded question answering and conversational retrieval over structured and unstructured data.
