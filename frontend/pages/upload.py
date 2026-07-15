import streamlit as st

from utils.session_state import initialize_session_state
from services.api_client import upload_document, get_namespaces


st.set_page_config(
    page_title="Upload Documents",
    page_icon="📤",
    layout="centered"
)


# Initialize
initialize_session_state()


st.title("📤 Upload Documents")
st.markdown("Add documents to your knowledge base")

st.divider()


# Load namespaces
try:
    namespace_response = get_namespaces()
    namespaces = namespace_response.get("namespaces", [])
except Exception as error:
    st.error(f"Error loading namespaces: {error}")
    namespaces = []


# Namespace selection
namespace = st.selectbox(
    "Select namespace:",
    namespaces if namespaces else ["No namespaces available"],
    disabled=not namespaces
)

st.divider()

# File upload section
st.subheader("📁 Select File")

uploaded_file = st.file_uploader(
    "Choose a document (PDF, CSV, TXT, DOCX)",
    type=["pdf", "csv", "txt", "docx"],
    help="Supported formats: PDF, CSV, TXT, DOCX"
)


# Upload button
if uploaded_file:
    st.write(f"**File:** {uploaded_file.name}")
    st.write(f"**Size:** {uploaded_file.size / 1024:.2f} KB")
    
    st.divider()
    
    if st.button("🚀 Upload Document", use_container_width=True):
        
        if namespace == "No namespaces available":
            st.error("Please select a valid namespace")
        else:
            with st.spinner("Uploading and processing document..."):
                try:
                    response = upload_document(
                        uploaded_file,
                        namespace
                    )
                    
                    st.success(f"Document uploaded successfully!")
                    st.json(response)
                
                except Exception as error:
                    st.error(f"Upload failed: {error}")

else:
    st.info("👆 Upload a document to get started")


st.divider()

# Info section
with st.expander("ℹ️ Upload Information"):
    st.markdown("""
    ### Supported Formats
    - **PDF**: Documents and reports
    - **CSV**: Structured data and datasets
    - **TXT**: Plain text files
    - **DOCX**: Microsoft Word documents
    
    ### Process
    1. Select target namespace
    2. Choose document file
    3. Click Upload
    4. System will extract and index content
    5. Use in chat queries immediately
    """)
