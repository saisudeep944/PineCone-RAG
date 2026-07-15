from app.services.llm.llm_service import (
    generate_answer
)


def should_rewrite_query(
    query
):

    prompt = f"""

You are a query rewrite detection system.

Determine whether the user's query
requires conversational rewriting
for semantic retrieval.

ONLY return:

yes
or
no

Rewrite is needed ONLY if:
- the query contains ambiguous references
- pronouns like it/this/that
- missing conversational context

Rewrite is NOT needed if:
- the query is already understandable
- important entities already exist
- the topic is already clear

User Query:

{query}
"""

    response = generate_answer(
        prompt
    ).strip().lower()

    return response == "yes"