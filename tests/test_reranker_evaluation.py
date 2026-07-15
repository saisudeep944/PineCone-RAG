from app.services.retrieval_service import (
    retrieve_documents
)

from app.services.hybrid.reranker_service import (
    rerank_results
)

from app.services.evaluation.retrieval_metrics import (
    precision_at_k
)

query = """
What does the document say about AI?
"""

# Ground truth labels
relevant_chunk_ids = [

    "d2b36833-7545-4c09-bb9d-6753319caf66_1",

    "d2b36833-7545-4c09-bb9d-6753319caf66_21"
]

# =====================================
# Stage 1 — Raw Retrieval
# =====================================

raw_results = retrieve_documents(

    query=query,

    namespace="AI_Medical_Device",

    top_k=5
)

raw_precision = precision_at_k(

    retrieved_chunks=raw_results,

    relevant_chunk_ids=
    relevant_chunk_ids,

    k=5
)

# =====================================
# Stage 2 — Reranked Retrieval
# =====================================

reranked = rerank_results(

    query=query,

    retrieved_chunks=raw_results,

    top_k=5
)

# Convert reranked structure
reranked_chunks = [

    item["chunk"]
    for item in reranked
]

reranked_precision = precision_at_k(

    retrieved_chunks=
    reranked_chunks,

    relevant_chunk_ids=
    relevant_chunk_ids,

    k=5
)

# =====================================
# Results
# =====================================

print("\nRAW RETRIEVAL PRECISION@5:\n")

print(raw_precision)

print("\nRERANKED PRECISION@5:\n")

print(reranked_precision)

print("\nRERANKER LIFT:\n")

print(
    reranked_precision
    -
    raw_precision
)