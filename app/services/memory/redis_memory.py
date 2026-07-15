import json
import os  # Added to read system environment variables
import redis

# =====================================
# AUTOMATIC CLOUD & LOCAL REDIS CONFIG
# =====================================
# Looks for Render's cloud connection string first. Falls back to localhost if not found.
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")

# Initialize client connection parameters securely
redis_client = redis.from_url(REDIS_URL, decode_responses=True)


def save_message(session_id, user_message, assistant_message):
    key = f"chat:{session_id}"
    existing = redis_client.get(key)

    if existing:
        history = json.loads(existing)
    else:
        history = []

    history.append({"user": user_message, "assistant": assistant_message})

    redis_client.set(key, json.dumps(history))


def load_conversation(session_id):
    key = f"chat:{session_id}"
    existing = redis_client.get(key)

    if not existing:
        return []

    return json.loads(existing)
