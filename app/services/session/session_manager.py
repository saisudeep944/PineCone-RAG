import uuid
import json
import redis

from datetime import datetime


redis_client = redis.Redis(

    host="localhost",

    port=6379,

    decode_responses=True
)

SESSION_TTL = 3600


# =====================================
# Create Session
# =====================================

def create_session(

    namespace
):

    session_id = str(
        uuid.uuid4()
    )

    session_key = (
        f"session:{session_id}"
    )

    redis_client.hset(

        session_key,

        mapping={

            "session_id":
            session_id,

            "created_at":
            str(datetime.utcnow()),

            "last_active":
            str(datetime.utcnow()),

            "message_count":
            0,

            "active_namespace":
            namespace,

            "status":
            "active"
        }
    )

    redis_client.expire(

        session_key,

        SESSION_TTL
    )

    return session_id


# =====================================
# Validate Session
# =====================================

def validate_session(

    session_id
):

    session = redis_client.hgetall(

        f"session:{session_id}"
    )

    return bool(session)


# =====================================
# Get Session Metadata
# =====================================

def get_session_metadata(

    session_id
):

    session = redis_client.hgetall(

        f"session:{session_id}"
    )

    if not session:

        return None

    return session


# =====================================
# Refresh Session
# =====================================

def refresh_session(

    session_id
):

    session_key = (
        f"session:{session_id}"
    )

    session = redis_client.hgetall(

        session_key
    )

    if not session:

        return

    current_count = int(

        session.get(
            "message_count",
            0
        )
    )

    redis_client.hset(

        session_key,

        mapping={

            "last_active":
            str(datetime.utcnow()),

            "message_count":
            current_count + 1
        }
    )

    redis_client.expire(

        session_key,

        SESSION_TTL
    )


# =====================================
# Delete Session
# =====================================

def delete_session(

    session_id
):

    redis_client.delete(

        f"session:{session_id}"
    )

    redis_client.delete(

        f"chat:{session_id}"
    )


# =====================================
# Deactivate Session
# =====================================

def deactivate_session(

    session_id
):

    session_key = (
        f"session:{session_id}"
    )

    redis_client.hset(

        session_key,

        "status",

        "inactive"
    )


# =====================================
# Update Active Namespace
# =====================================

def update_active_namespace(

    session_id,

    namespace
):

    session_key = (
        f"session:{session_id}"
    )

    redis_client.hset(

        session_key,

        "active_namespace",

        namespace
    )

   


# =====================================
# Save Message
# =====================================

def save_message(

    session_id,

    role,

    content
):

    history_key = (
        f"history:{session_id}"
    )

    message = {

        "role":
        role,

        "content":
        content
    }

    redis_client.rpush(

        history_key,

        json.dumps(message)
    )


# =====================================
# Get Conversation History
# =====================================

def get_conversation_history(

    session_id
):

    history_key = (
        f"history:{session_id}"
    )

    messages = redis_client.lrange(

        history_key,

        0,

        -1
    )

    return [

        json.loads(msg)

        for msg in messages
    ]

# =====================================
# List Sessions
# =====================================

def list_sessions():

    session_keys = redis_client.keys(
        "session:*"
    )

    sessions = []

    for key in session_keys:

        metadata = redis_client.hgetall(
            key
        )

        sessions.append({

            "session_id":
            metadata.get(
                "session_id"
            ),

            "active_namespace":
            metadata.get(
                "active_namespace"
            ),

            "created_at":
            metadata.get(
                "created_at"
            ),

            "last_active":
            metadata.get(
                "last_active"
            ),

            "message_count":
            metadata.get(
                "message_count"
            ),

            "status":
            metadata.get(
                "status"
            )
        })

    sessions.sort(

        key=lambda x:
        x["last_active"],

        reverse=True
    )

    return sessions