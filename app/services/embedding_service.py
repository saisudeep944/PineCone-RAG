import os
import requests

# 1. Grab your free Hugging Face token from environment variables
HF_TOKEN = os.environ.get("HF_TOKEN")

# 2. CORRECTED: Path to the specific serverless endpoint for your target model
API_URL = "https://huggingface.co"


def generate_embeddings(texts: list):
    # Ensure it always handles a list format
    if isinstance(texts, str):
        texts = [texts]

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": texts, "options": {"wait_for_model": True}}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        # 3. CORRECTED: Removed .tolist(). The API already sends a standard list back.
        embeddings = response.json()
        return embeddings

    except Exception as e:
        raise RuntimeError(
            f"Failed to generate embeddings from Hugging Face API: {e}"
        )
