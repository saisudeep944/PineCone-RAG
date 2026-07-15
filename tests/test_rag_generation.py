from app.services.retrieval_service import (
    retrieve_documents
)

from app.services.hybrid.reranker_service import (
    rerank_results
)

from app.services.llm.prompt_builder import (
    build_rag_prompt
)

from app.services.llm.llm_service import (
    generate_answer
)
from app.services.llm.response_formatter import (
    format_rag_response
)
from app.services.llm.guardrails import (
    validate_retrieval_confidence
)
from app.services.llm.conversation_memory import (
    conversation_history
)
from app.services.llm.query_rewriter import (
    rewrite_query
)

query = """
What does the document say about AI?
"""

rewritten_query = rewrite_query(
    query
)

print("\nREWRITTEN QUERY:\n")

print(rewritten_query)

# ====================================
# Retrieval
# ====================================

results = retrieve_documents(

    query=rewritten_query,

    namespace="AI_Medical_Device",

    top_k=5
)

# ====================================
# Reranking
# ====================================

reranked = rerank_results(

    query=rewritten_query,

    retrieved_chunks=results,

    top_k=3
)

reranked_chunks = [

    item["chunk"]
    for item in reranked
]

# ====================================
# Prompt Construction
# ====================================

prompt = build_rag_prompt(

    query=query,

    retrieved_chunks=
    reranked_chunks
)

# ====================================
# LLM Generation
# ====================================

answer = generate_answer(
    prompt
)

print("\nFINAL ANSWER:\n")

formatted_response = (
    format_rag_response(

        answer=answer,

        retrieved_chunks=
        reranked_chunks
    )
)

print(formatted_response)


conversation_history.append(

    {

        "user": query,

        "assistant": answer
    }
)
print("\nCONVERSATION HISTORY:\n",conversation_history)