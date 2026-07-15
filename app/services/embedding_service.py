from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

def generate_embeddings(texts: list):

    embeddings = model.encode(texts)

    return embeddings.tolist()