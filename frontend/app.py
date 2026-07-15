import streamlit as st
import json
from datetime import datetime
import os

from utils.session_state import initialize_session_state
from services.api_client import (
    create_session,
    get_namespaces,
    list_sessions,
    stream_chat
)

BACKEND_URL = os.environ.get("BACKEND_URL")

# 2. Check st.secrets only if running on Streamlit Cloud, default to local if neither exists
if not BACKEND_URL:
    if "BACKEND_URL" in getattr(st, "secrets", {}):
        BACKEND_URL = st.secrets["BACKEND_URL"]
    else:
        BACKEND_URL = "http://127.0.0.1:8000"


# ==========================================
# Helper Functions
# ==========================================

def format_markdown_response(text: str) -> str:
    """
    Format response text for better markdown rendering.
    Handles proper spacing, lists, and code blocks.
    """
    if not text:
        return ""
    
    # Ensure proper spacing around headers
    text = text.replace("\n#", "\n\n#")
    text = text.replace("##", "\n##")
    
    # Ensure proper spacing around bullet points
    text = text.replace("\n- ", "\n\n- ")
    text = text.replace("\n* ", "\n\n* ")
    text = text.replace("\n• ", "\n\n• ")
    
    # Ensure proper spacing around numbered lists
    import re
    text = re.sub(r'\n(\d+\.)', r'\n\n\1', text)
    
    return text


# ==========================================
# Streamlit Config
# ==========================================

st.set_page_config(
    page_title="Enterprise RAG Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# Load CSS
# ==========================================

import os
css_path = os.path.join(os.path.dirname(__file__), "styles/custom.css")
with open(css_path) as css_file:
    st.markdown(
        f"<style>{css_file.read()}</style>",
        unsafe_allow_html=True
    )


# ==========================================
# Initialize Session State
# ==========================================

initialize_session_state()


# ==========================================
# Load Namespaces
# ==========================================

try:
    namespace_response = get_namespaces()
    st.session_state.available_namespaces = (
        namespace_response.get("namespaces", [])
    )
    
    # Set first namespace as default if not set
    if (st.session_state.active_namespace is None and 
        st.session_state.available_namespaces):
        st.session_state.active_namespace = st.session_state.available_namespaces[0]
except Exception as error:
    st.error(f"Error loading namespaces: {error}")
    st.session_state.available_namespaces = []


# ==========================================
# Sidebar
# ==========================================

with st.sidebar:
    
    # Logo & Title
    st.markdown("""
        <div class="sidebar-header">
            <h1>🤖 Enterprise RAG</h1>
            <p class="sidebar-subtitle">Conversational AI Workspace</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Namespace Selection
    st.subheader("📁 Namespace")
    
    if st.session_state.available_namespaces:
        # Get current index safely
        try:
            current_index = st.session_state.available_namespaces.index(
                st.session_state.active_namespace
            )
        except (ValueError, IndexError):
            current_index = 0
        
        selected_namespace = st.selectbox(
            "Select Knowledge Base",
            st.session_state.available_namespaces,
            index=current_index,
            label_visibility="collapsed",
            key="namespace_selector"  
        )
        
        # If namespace changed, create new session
        if selected_namespace != st.session_state.active_namespace:
            st.session_state.active_namespace = selected_namespace
            st.session_state.messages = []  # Clear messages first
            st.session_state.session_id = None  # Reset session
            try:
                session_response = create_session(st.session_state.active_namespace)
                st.session_state.session_id = session_response["session_id"]
                st.success(f"✓ Switched to {selected_namespace}")
                st.rerun()
            except Exception as error:
                st.error(f"Error switching namespace: {error}")
    else:
        st.warning("⚠️ No namespaces available. Create documents first.")
    
    # Create New Session Button
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("➕ New Chat", use_container_width=True):
            try:
                session_response = create_session(
                    st.session_state.active_namespace
                )
                st.session_state.session_id = session_response["session_id"]
                st.session_state.messages = []
                st.success("New session created!")
                st.rerun()
            except Exception as error:
                st.error(f"Error creating session: {error}")
    
    with col2:
        if st.button("🔄 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    st.divider()
    
    # Session List
    st.subheader("💬 Recent Sessions")
    
    try:
        sessions_response = list_sessions()
        sessions = sessions_response.get("sessions", [])
        
        if sessions:
            for i, session in enumerate(sessions[:5]):  # Show top 5
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.caption(f"📌 {session['active_namespace']}")
                        st.code(session["session_id"][:12] + "...", language="text")
                    
                    with col2:
                        if st.button("📂", key=f"session_{i}", help="Load session"):
                            st.session_state.session_id = session["session_id"]
                            st.session_state.active_namespace = session.get("active_namespace", st.session_state.active_namespace)
                            st.session_state.messages = []
                            st.success(f"✓ Loaded session from {session.get('active_namespace', 'Unknown')}")
                            st.rerun()
                    st.divider()
        else:
            st.info("No sessions yet. Create one to get started!")
    
    except Exception as error:
        st.error(f"Error loading sessions: {error}")
    
    st.divider()
    
    # Debug Info
    with st.expander("🔍 Debug Info", expanded=False):
        st.write(f"**Available Namespaces:** {len(st.session_state.available_namespaces)}")
        if st.session_state.available_namespaces:
            st.write(st.session_state.available_namespaces)
        st.write(f"**Active Namespace:** {st.session_state.active_namespace}")
        st.write(f"**Session ID:** {st.session_state.session_id[:8] if st.session_state.session_id else 'None'}...")
    
    st.divider()
    
    # Info Section
    st.markdown("""
        <div class="sidebar-footer">
            <p><strong>Tips:</strong></p>
            <ul>
                <li>Select a namespace to organize documents</li>
                <li>Each new chat maintains conversation history</li>
                <li>Ask questions about your uploaded documents</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)


# ==========================================
# Main Chat Area
# ==========================================

# Header
st.markdown("""
    <div class="main-header">
        <h1>💬 AI Chat Assistant</h1>
        <p>Ask questions about your documents using our advanced RAG system</p>
    </div>
""", unsafe_allow_html=True)


# ==========================================
# Auto Session Creation
# ==========================================

if st.session_state.session_id is None and st.session_state.active_namespace:
    try:
        session_response = create_session(
            st.session_state.active_namespace
        )
        st.session_state.session_id = session_response["session_id"]
    except Exception as error:
        st.error(f"Error creating session: {error}")
elif st.session_state.session_id is None:
    st.warning("⚠️ Please wait for namespaces to load...")


# ==========================================
# Display Chat Messages
# ==========================================

message_container = st.container()

with message_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                # Format and render markdown content properly
                formatted_content = format_markdown_response(message["content"])
                st.markdown(formatted_content)
                
                # Display sources if available
                if "sources" in message and message["sources"]:
                    with st.expander("📚 View Sources"):
                        for i, source in enumerate(message["sources"], 1):
                            st.markdown(f"""
                                <div class="source-card">
                                    <p><strong>📄 {source.get('file_name', 'Unknown')}</strong></p>
                                    <p class="source-meta">Chunk #{source.get('chunk_index', '?')} • Score: {source.get('rerank_score', 0):.3f}</p>
                                    <p class="source-text">{source.get('text', '')[:200]}...</p>
                                </div>
                            """, unsafe_allow_html=True)
            else:
                st.markdown(message["content"])


# ==========================================
# Chat Input
# ==========================================

st.divider()

prompt = st.chat_input(
    "Ask something about your documents...",
    key="chat_input"
)


# ==========================================
# User Prompt Handling
# ==========================================

if prompt:
    
    # Add user message to state
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get assistant response
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        response_metadata = {}
        first_token = True
        
        try:
            # Stream the response
            for line in stream_chat(
                st.session_state.session_id,
                prompt
            ):
                if line.strip():
                    try:
                        event = json.loads(line)
                        
                        if event.get("type") == "token":
                            content = event.get("content", "")
                            if content:
                                if first_token:
                                    first_token = False
                                full_response += content
                                # Display with proper markdown formatting
                                formatted = format_markdown_response(full_response)
                                response_container.markdown(formatted + " ▌")
                        
                        elif event.get("type") == "metadata":
                            response_metadata = event
                        
                        elif event.get("type") == "complete":
                            pass  # Stream complete
                    
                    except json.JSONDecodeError:
                        continue
            
            # Final update with formatted markdown
            formatted_response = format_markdown_response(full_response)
            response_container.markdown(formatted_response)
            
            # Save complete response to state
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response,
                "sources": response_metadata.get("sources", []),
                "intent": response_metadata.get("intent", "")
            })
            
            # Display sources if available
            if response_metadata.get("sources"):
                with st.expander("📚 View Sources"):
                    for i, source in enumerate(response_metadata.get("sources", []), 1):
                        st.markdown(f"""
                            <div class="source-card">
                                <p><strong>📄 {source.get('file_name', 'Unknown')}</strong></p>
                                <p class="source-meta">Chunk #{source.get('chunk_index', '?')} • Score: {source.get('rerank_score', 0):.3f}</p>
                                <p class="source-text">{source.get('text', '')[:200]}...</p>
                            </div>
                        """, unsafe_allow_html=True)
        
        except Exception as error:
            st.error(f"Error streaming response: {error}")
            st.session_state.messages.pop()  # Remove incomplete user message


# ==========================================
# Footer
# ==========================================

st.divider()

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    ns_display = st.session_state.active_namespace or "Loading..."
    st.caption(f"📌 Namespace: **{ns_display}**")

with footer_col2:
    st.caption(f"💬 Messages: **{len(st.session_state.messages)}**")

with footer_col3:
    st.caption(f"🕐 {datetime.now().strftime('%H:%M:%S')}")


# ==========================================
# Chat Input
# ==========================================

prompt = st.chat_input(
    "Ask something about your documents..."
)


# ==========================================
# User Prompt Handling
# ==========================================

if prompt:

    # ======================================
    # Add User Message
    # ======================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    with st.chat_message("user"):

        st.markdown(prompt)


    # ======================================
    # Assistant Response
    # ======================================

    with st.chat_message("assistant"):

        response_container = st.empty()

        full_response = ""

        try:

            for chunk in stream_chat(
                st.session_state.session_id,
                prompt
            ):

                full_response += chunk

                response_container.markdown(
                    full_response
                )


            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response
                }
            )

        except Exception as error:

            st.error(
                f"Streaming Error: {error}"
            )