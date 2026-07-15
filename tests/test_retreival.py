from app.services.retrieval_service import (
    retrieve_documents
)

query = "What does the document say about AI?"

results = retrieve_documents(
    query=query,
    namespace="AI_Medical_Device",
)


print("\nRETRIEVED RESULTS:\n")

for result in results:

    print("=" * 80)

    print(f"Score: {result['score']}")

    print(f"File: {result['file_name']}")

    print(f"Chunk Index: {result['chunk_index']}")

    print("\nTEXT:\n")

    print(result["text"])