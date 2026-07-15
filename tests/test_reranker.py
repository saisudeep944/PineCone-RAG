from app.services.retrieval_service import (
    retrieve_documents
)

from app.services.hybrid.reranker_service import (
    rerank_results
)

query = """
What does the document say about AI?
"""


# Broad retrieval
results = retrieve_documents(
    query=query,
    namespace="AI_Medical_Device",
    top_k=10
)
print(len(results))
print(results)

# Reranking
reranked = rerank_results(
    query=query,
    retrieved_chunks=results,
    top_k=5
)

print("\nRERANKED RESULTS:\n")

for item in reranked:

    chunk = item["chunk"]

    print("=" * 80)

    print(
        f"Rerank Score: "
        f"{item['rerank_score']}"
    )

    print(
        f"File: "
        f"{chunk['file_name']}"
    )

    print("\nTEXT:\n")

    print(chunk["text"])