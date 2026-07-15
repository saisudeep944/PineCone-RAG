import os

from app.services.ingestion_service import (
    load_document,
    chunk_text
)

from app.services.hybrid.bm25_service import (
    BM25Retriever
)

from app.services.retrieval_service import (
    retrieve_documents
)

from app.services.hybrid.fusion_service import (
    reciprocal_rank_fusion
)

# Load local chunks
file_path = "data/AI_Medical_Device.pdf"

text = load_document(file_path)

file_name = os.path.basename(file_path)

source_type = file_name.split(".")[-1]

chunks = chunk_text(
    text=text,
    file_name=file_name,
    source_type=source_type
)

# BM25 retrieval
bm25 = BM25Retriever(chunks)

query = "stock market decline"

bm25_results = bm25.search(query)

# Vector retrieval
vector_results = retrieve_documents(
    query=query,
    namespace="AI_Medical_Device",
)

# Fusion
fused = reciprocal_rank_fusion(
    vector_results,
    bm25_results
)

print("\nFUSED RESULTS:\n")

for chunk_id, score in fused:

    print(f"{chunk_id} → {score}")