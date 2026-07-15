from app.services.memory.redis_memory import (
    load_conversation
)

from app.services.llm.llm_service import (
    generate_answer
)


def rewrite_query(

    session_id,

    current_query
):

    conversation_history = (
        load_conversation(
            session_id
        )
    )

    if not conversation_history:

        return current_query

    previous_user_queries = "\n".join(

        [

            f"User: {item['user']}"

            for item in conversation_history[-3:]
        ]
    )

    rewrite_prompt = f"""

You are an enterprise retrieval
query rewriting system.

Your task is to rewrite
the user's latest message
into a standalone retrieval query.

IMPORTANT RULES:

1. You can previous USER questions
   as context.

2. NEVER use assistant responses
   as factual grounding.

3. Preserve topic continuity.

4. Avoid adding information
   that is not explicitly present
   in the conversation history.

5. If the current query is already
   understandable, return it unchanged.

6. Avoid over-specific assumptions.

Conversation History:

{previous_user_queries}

Current User Question:

{current_query}

Return ONLY the rewritten query.
"""

    rewritten_query = generate_answer(
        rewrite_prompt
    )

    return rewritten_query.strip()