from app.services.llm.llm_service import (
    generate_answer
)


VALID_INTENTS = [

    "retrieval",

    "gratitude",

    "acknowledgement",

    "greeting",

    "exit",

    "smalltalk"
]


def classify_intent(
    user_message
):

    prompt = f"""

You are an intent classification system.

Classify the user's message into ONLY one
of the following intents:

retrieval
gratitude
acknowledgement
greeting
exit
smalltalk

User Message:

{user_message}

Return ONLY the intent label.

Do NOT explain anything.
"""

    intent = generate_answer(
        prompt
    ).strip().lower()

    if intent not in VALID_INTENTS:

        return "smalltalk"

    return intent