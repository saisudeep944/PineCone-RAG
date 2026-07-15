import streamlit as st


# ==========================================
# Initialize Session State
# ==========================================

def initialize_session_state():
    """Initialize all required session state variables for the Streamlit app."""
    
    # Messages in current chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Current session ID
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    
    # Active namespace for document organization
    if "active_namespace" not in st.session_state:
        st.session_state.active_namespace = None
    
    # Available namespaces from backend
    if "available_namespaces" not in st.session_state:
        st.session_state.available_namespaces = []
    
    # UI state for expanders
    if "show_sources" not in st.session_state:
        st.session_state.show_sources = {}
    
    # Loading state during streaming
    if "is_loading" not in st.session_state:
        st.session_state.is_loading = False
    
    # Last response metadata
    if "last_metadata" not in st.session_state:
        st.session_state.last_metadata = {}


def reset_messages():
    """Clear all messages from current session."""
    st.session_state.messages = []


def add_message(role: str, content: str, **kwargs):
    """Add a message to the conversation history.
    
    Args:
        role: "user" or "assistant"
        content: Message text
        **kwargs: Additional metadata (sources, intent, etc.)
    """
    message = {
        "role": role,
        "content": content,
        **kwargs
    }
    st.session_state.messages.append(message)


def get_messages():
    """Get all messages in current session."""
    return st.session_state.messages


def set_session_id(session_id: str):
    """Set the current session ID."""
    st.session_state.session_id = session_id


def set_namespace(namespace: str):
    """Set the active namespace."""
    st.session_state.active_namespace = namespace


def set_loading(is_loading: bool):
    """Set loading state."""
    st.session_state.is_loading = is_loading