from app.core.pinecone_client import index
import uuid

def store_embedding(text: str, embedding: list):

    vector_id = str(uuid.uuid4())

    index.upsert(
        vectors=[
            {
                "id": vector_id,
                "values": embedding,
                "metadata": {
                    "text": text
                }
            }
        ]
    )

    return vector_id

def search_embedding(query_embedding: list):

    results = index.query(
        vector=query_embedding,
        top_k=3,
        include_metadata=True
    )

    return results

def bulk_upsert(
    chunks: list,
    embeddings: list,
    namespace: str
):

    vectors = []

    for chunk, embedding in zip(chunks, embeddings):

        vector = {
            "id": chunk["chunk_id"],
            "values": embedding,
            "metadata": {
                "document_id": chunk["document_id"],
                "chunk_index": chunk["chunk_index"],
                "text": chunk["text"],
                "file_name": chunk["file_name"],
                "source_type": chunk["source_type"],
                "upload_time": chunk["upload_time"]
            }
        }

        vectors.append(vector)

    index.upsert(
        vectors=vectors,
        namespace=namespace
    )

    return len(vectors)