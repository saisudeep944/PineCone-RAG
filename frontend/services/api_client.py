import os
import requests
import streamlit as st

# ==============================================================================
# AUTOMATIC FRONTEND URL DETECTION
# ==============================================================================
# Looks for Render's environment variable first. Falls back to localhost for testing.
BASE_URL = os.environ.get("BACKEND_URL")

if not BASE_URL:
    if "BACKEND_URL" in getattr(st, "secrets", {}):
        BASE_URL = st.secrets["BACKEND_URL"]
    else:
        BASE_URL = "http://localhost:8000"


# ==========================================
# Session APIs
# ==========================================

def create_session(namespace: str):
    response = requests.post(
        f"{BASE_URL}/session/create",
        json={
            "namespace": namespace
        }
    )
    response.raise_for_status()
    return response.json()


def list_sessions():
    response = requests.get(
        f"{BASE_URL}/sessions"
    )
    response.raise_for_status()
    return response.json()


# ==========================================
# Namespace APIs
# ==========================================

def get_namespaces():
    response = requests.get(
        f"{BASE_URL}/namespaces"
    )
    response.raise_for_status()
    return response.json()


# ==========================================
# Upload APIs
# ==========================================

def upload_document(file, namespace: str):
    files = {
        "file": file
    }
    data = {
        "namespace": namespace
    }
    response = requests.post(
        f"{BASE_URL}/upload",
        files=files,
        data=data
    )
    response.raise_for_status()
    return response.json()


# ==========================================
# Streaming Chat API
# ==========================================

def stream_chat(session_id: str, message: str):
    # FIXED THE 422 ERROR HERE:
    # Changed "message": message -> "query": message to perfectly align with your backend Pydantic schema
    response = requests.post(
        f"{BASE_URL}/chat/stream",
        json={
            "session_id": session_id,
            "query": message
        },
        stream=True
    )

    response.raise_for_status()

    for chunk in response.iter_content(
        chunk_size=1024,
        decode_unicode=True
    ):
        if chunk:
            yield chunk
