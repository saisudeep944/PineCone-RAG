from app.services.retrieval_service import (
    retrieve_documents
)

from app.services.evaluation.retrieval_metrics import (
    precision_at_k
)

query = """
What does the document say about AI?
"""

results = retrieve_documents(
    query=query,
    namespace="AI_Medical_Device",
    top_k=5
)

# Ground truth relevant chunks
relevant_chunk_ids = [

    "d2b36833-7545-4c09-bb9d-6753319caf66_1",

    "d2b36833-7545-4c09-bb9d-6753319caf66_21"
]

score = precision_at_k(

    retrieved_chunks=results,

    relevant_chunk_ids=
    relevant_chunk_ids,

    k=5
)

print("\nPRECISION@5:\n")

print(score)