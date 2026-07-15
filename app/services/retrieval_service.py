from app.services.embedding_service import (
    generate_embeddings
)

from app.core.pinecone_client import index


def retrieve_documents(
    query: str,
    namespace: str,
    top_k: int = 5
    
):

    # Wrap query in list since generate_embeddings expects list of texts
    query_embeddings = generate_embeddings([query])
    query_embedding = query_embeddings[0]  # Extract single embedding

    results = index.query(
    vector=query_embedding,
    top_k=top_k,
    include_metadata=True,
    namespace=namespace
    )   

    retrieved_chunks = []

    for match in results["matches"]:
        
        retrieved_chunks.append({
            "chunk_id": match["id"],
            "score": match["score"],
            "text": match["metadata"]["text"],
            "file_name": match["metadata"]["file_name"],
            "chunk_index": match["metadata"]["chunk_index"],
            "document_id": match["metadata"]["document_id"]
            
        })

    return retrieved_chunks