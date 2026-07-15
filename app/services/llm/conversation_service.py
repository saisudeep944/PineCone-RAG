from app.services.llm.llm_service import (
    generate_answer
)


def generate_conversational_response(

    user_message,

    intent
):

    prompt = f"""

You are an enterprise AI assistant.

The user message was classified as:

{intent}

FORMATTING RULES:

1. Add ONE blank line before starting your response
2. Use proper markdown formatting:
   - **Bold text** for emphasis
   - Use headings if needed: ## Heading
   - Use bullet points: • Point 1, • Point 2
3. Add ONE blank line between paragraphs
4. Keep response concise and natural

RESPONSE RULES:

1. Be natural and conversational.
2. Sound like a modern AI copilot.
3. If you don't know the answer, say you don't know.
4. Keep it brief for conversational intents.

User Message:

{user_message}

RESPONSE:
"""

    response = generate_answer(
        prompt
    )

    return response