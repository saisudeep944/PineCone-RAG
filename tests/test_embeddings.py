from app.services.embedding_service import generate_embedding
from app.services.pinecone_service import (
    store_embedding,
    search_embedding
)

# Store text
text = "Pinecone is a vector database"

embedding = generate_embedding(text)

vector_id = store_embedding(text, embedding)

print(f"Stored vector ID: {vector_id}")

# Query text
query = "What is a vector DB?"

query_embedding = generate_embedding(query)

results = search_embedding(query_embedding)

print(results)