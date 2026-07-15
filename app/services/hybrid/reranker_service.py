import os
import requests

# 1. Grab your free Hugging Face token from environment variables
HF_TOKEN = os.environ.get("HF_TOKEN")

# 2. Target the specific serverless endpoint for the ms-marco cross-encoder
API_URL = "https://huggingface.co"


def rerank_results(query, retrieved_chunks, top_k=5):
    # Prepare the query-text pairs exactly how the Hugging Face API expects them
    pairs = [
        {"text": query, "text_pair": chunk["text"]} for chunk in retrieved_chunks
    ]

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": pairs, "options": {"wait_for_model": True}}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        # The API directly returns a list of dictionaries containing scores: [{"score": 0.99}, ...]
        api_results = response.json()

        reranked = []
        for chunk, api_res in zip(retrieved_chunks, api_results):
            # Extract the raw score float from the API response
            score = api_res.get("score", 0.0)

            reranked.append({"chunk": chunk, "rerank_score": float(score)})

        # Sort results by the highest rerank score descending
        reranked.sort(key=lambda x: x["rerank_score"], reverse=True)

        print("\nRAW RETRIEVED CHUNKS:\n", retrieved_chunks)
        print("\nFINAL RERANKED RESULTS:\n", reranked)

        return reranked[:top_k]

    except Exception as e:
        raise RuntimeError(f"Failed to rerank results via Hugging Face API: {e}")
