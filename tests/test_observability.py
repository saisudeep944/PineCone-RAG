from app.services.retrieval_service import (
    retrieve_documents
)

from app.services.hybrid.reranker_service import (
    rerank_results
)

from app.services.observability.trace_service import (
    build_trace
)

query = """
What does the document say about AI?
"""

# Retrieval
results = retrieve_documents(
    query=query,
    namespace="AI_Medical_Device",
    top_k=10
)

# Reranking
reranked = rerank_results(
    query=query,
    retrieved_chunks=results,
    top_k=5
)

print("\nRETRIEVAL TRACES:\n")

for item in reranked:

    chunk = item["chunk"]

    trace = build_trace(

        query=query,

        chunk=chunk,

        vector_score=chunk.get("score"),

        rerank_score=item[
            "rerank_score"
        ],

        namespace=
        "AI_Medical_Device",

        retrieval_stage=
        "reranked"
    )

    print("=" * 80)

    for key, value in trace.items():

        print(f"{key}: {value}")