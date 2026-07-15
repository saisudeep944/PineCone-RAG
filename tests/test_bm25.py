import os

from app.services.ingestion_service import (
    load_document,
    chunk_text
)

from app.services.hybrid.bm25_service import (
    BM25Retriever
)

file_path = "data/AI_Medical_Device.pdf"

text = load_document(file_path)

file_name = os.path.basename(file_path)

source_type = file_name.split(".")[-1]

chunks = chunk_text(
    text=text,
    file_name=file_name,
    source_type=source_type
)

retriever = BM25Retriever(chunks)

query = "open high close"

results = retriever.search(query)

print("\nBM25 RESULTS:\n")

for chunk, score in results:

    print("=" * 80)

    print(f"BM25 Score: {score}")

    print(f"File: {chunk['file_name']}")

    print("\nTEXT:\n")

    print(chunk["text"])