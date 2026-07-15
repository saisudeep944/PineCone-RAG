from app.services.retrieval_service import (
    retrieve_documents
)

from app.services.hybrid.reranker_service import (
    rerank_results
)

from app.services.evaluation.retrieval_metrics import (
    mean_reciprocal_rank
)

query = """
What does the document say about AI?
"""

relevant_chunk_ids = [

    "d2b36833-7545-4c09-bb9d-6753319caf66_1",

    "d2b36833-7545-4c09-bb9d-6753319caf66_21"
]

# =====================================
# Raw Retrieval
# =====================================

raw_results = retrieve_documents(

    query=query,

    namespace="AI_Medical_Device",

    top_k=5
)

raw_mrr = mean_reciprocal_rank(

    retrieved_chunks=
    raw_results,

    relevant_chunk_ids=
    relevant_chunk_ids
)

# =====================================
# Reranked Retrieval
# =====================================

reranked = rerank_results(

    query=query,

    retrieved_chunks=
    raw_results,

    top_k=5
)

reranked_chunks = [

    item["chunk"]
    for item in reranked
]

reranked_mrr = mean_reciprocal_rank(

    retrieved_chunks=
    reranked_chunks,

    relevant_chunk_ids=
    relevant_chunk_ids
)

# =====================================
# Results
# =====================================

print("\nRAW MRR:\n")

print(raw_mrr)

print("\nRERANKED MRR:\n")

print(reranked_mrr)

print("\nMRR IMPROVEMENT:\n")

print(
    reranked_mrr
    -
    raw_mrr
)