from app.core.chat_engine import (
    process_chat_message
)

from app.services.session.session_manager import (

    create_session,

    get_session_metadata
)


# =========================================
# Dynamic Namespace
# =========================================

namespace = (
    "AI_Medical_Device"
)

# =========================================
# Session Creation
# =========================================

session_id = create_session(
    namespace=namespace
)

print("\nSESSION CREATED:\n")

print(session_id)

metadata = (
    get_session_metadata(
        session_id
    )
)

print(
    "\nSESSION METADATA:\n"
)

print(metadata)

print(
    "\nENTERPRISE CONVERSATIONAL RAG\n"
)

# =========================================
# Chat Loop
# =========================================

while True:

    user_message = input(
        "\nUSER: "
    )

    response = (
        process_chat_message(

            session_id,

            user_message
        )
    )

    print(
        "\nASSISTANT:\n"
    )

    print(
        response["answer"]
    )

    if response["status"] == "terminated":

        break