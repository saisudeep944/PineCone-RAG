import json

import redis


redis_client = redis.Redis(

    host="localhost",

    port=6379,

    decode_responses=True
)


def save_message(

    session_id,

    user_message,

    assistant_message
):

    key = f"chat:{session_id}"

    existing = redis_client.get(key)

    if existing:

        history = json.loads(existing)

    else:

        history = []

    history.append(

        {

            "user":
            user_message,

            "assistant":
            assistant_message
        }
    )

    redis_client.set(

        key,

        json.dumps(history)
    )


def load_conversation(
    session_id
):

    key = f"chat:{session_id}"

    existing = redis_client.get(key)

    if not existing:

        return []

    return json.loads(existing)