import os
from huggingface_hub import InferenceClient

# 1. Initialize using your exact requested provider pattern
client = InferenceClient(
    provider="hf-inference",
    api_key=os.environ.get("HF_TOKEN"),
)


def generate_embeddings(texts: list):
    if isinstance(texts, str):
        texts = [texts]

    try:
        # 2. Generates structural float coordinate arrays instead of text mappings
        embeddings = client.feature_extraction(
            text=texts, model="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Convert return format to a native python list safely
        if hasattr(embeddings, "tolist"):
            return embeddings.tolist()

        return list(embeddings)

    except Exception as e:
        raise RuntimeError(
            f"Failed to generate embeddings from Hugging Face Client: {e}"
        )
