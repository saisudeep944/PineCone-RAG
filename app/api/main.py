from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import (
    StreamingResponse
)
from app.core.chat_engine import (
    stream_chat_response
)
from app.api.schemas import (

    CreateSessionRequest,

    CreateSessionResponse,

    ChatRequest,

    ChatResponse
)

from app.services.session.session_manager import (

    create_session
)

from app.core.chat_engine import (
    process_chat_message
)
from app.core.namespace_service import (
    namespace_exists
)
from app.core.namespace_service import (

    namespace_exists,

    list_namespaces
)
from app.services.session.session_manager import (
    update_active_namespace
)
from app.api.schemas import (
    SwitchNamespaceRequest
)
from fastapi import UploadFile

from fastapi import File
from app.services.upload.upload_service import (
    process_uploaded_file
)
from app.services.session.session_manager import (
    get_conversation_history
)
from app.services.session.session_manager import (
    list_sessions
)
from fastapi.middleware.cors import (
    CORSMiddleware
)

app = FastAPI(

    title="Enterprise Conversational RAG",

    version="1.0.0"
)
# =========================================
# CORS Configuration
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================
# Health Endpoint
# =========================================

@app.get("/health")
def health_check():

    return {

        "status":
        "healthy"
    }


# =========================================
# Create Session Endpoint
# =========================================

@app.post(

    "/session/create",

    response_model=
    CreateSessionResponse
)

def create_chat_session(

    request:
    CreateSessionRequest
):
    if not namespace_exists(
    request.namespace):

        raise HTTPException(

            status_code=400,

            detail=
            "Namespace does not exist in Pinecone."
        )

    session_id = create_session(

        namespace=
        request.namespace
    )

    return {

        "session_id":
        session_id,

        "namespace":
        request.namespace
    }


# =========================================
# Chat Endpoint
# =========================================

@app.post(

    "/chat",

    response_model=
    ChatResponse
)

def chat(

    request:
    ChatRequest
):

    try:

        result = (
            process_chat_message(

                session_id=
                request.session_id,

                user_message=
                request.message
            )
        )

        return {

            "status":
            result["status"],

            "intent":
            result["intent"],

            "answer":
            result["answer"],

            "sources":
            result["sources"]
        }

    except Exception as e:

        import traceback

        print("\nCHAT ENDPOINT ERROR:\n")

        traceback.print_exc()

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )

# =========================================
# Streaming Chat Endpoint
# =========================================

@app.post("/chat/stream")

async def stream_chat(

    request: ChatRequest
):

    async def event_generator():

        response = process_chat_message(

            session_id=request.session_id,

            user_message=request.message
        )

        words = response["answer"].split()

        for word in words:

            yield word + " "

    return StreamingResponse(

        event_generator(),

        media_type="text/plain"
    )
# =========================================
# List Namespaces
# =========================================

@app.get("/namespaces")
def get_namespaces():

    namespaces = (
        list_namespaces()
    )

    return {

        "namespaces":
        namespaces
    }

# =========================================
# Switch Active Namespace
# =========================================

@app.post(
    "/session/switch-namespace"
)

def switch_namespace(

    request:
    SwitchNamespaceRequest
):

    if not namespace_exists(
        request.namespace
    ):

        raise HTTPException(

            status_code=400,

            detail=
            "Namespace does not exist."
        )

    update_active_namespace(

        session_id=
        request.session_id,

        namespace=
        request.namespace
    )

    return {

        "status":
        "success",

        "active_namespace":
        request.namespace
    }



# =========================================
# Get Conversation History
# =========================================

@app.get(
    "/session/history/{session_id}"
)

def session_history(

    session_id: str
):

    messages = (
        get_conversation_history(
            session_id
        )
    )

    return {

        "session_id":
        session_id,

        "messages":
        messages
    }

# =========================================
# List Sessions
# =========================================

@app.get("/sessions")
def get_sessions():

    sessions = (
        list_sessions()
    )

    return {

        "sessions":
        sessions
    }

    # =========================================
# Upload Document
# =========================================

@app.post("/upload")
def upload_document(

    file: UploadFile = File(...)
):

    result = process_uploaded_file(
        file
    )

    return {

        "status":
        "success",

        "file_name":
        result["file_name"],

        "namespace":
        result["namespace"]
    }