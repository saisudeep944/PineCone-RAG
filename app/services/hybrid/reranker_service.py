import os
from huggingface_hub import InferenceClient

# 1. Initialize the Inference Client exactly as requested
client = InferenceClient(
    provider="hf-inference",
    api_key=os.environ["HF_TOKEN"],
)


def rerank_results(query, retrieved_chunks, top_k=5):
    # If there are no chunks retrieved, return an empty list immediately
    if not retrieved_chunks:
        return []

    # 2. FIXED: Format pairs as explicit dictionaries to satisfy Hugging Face pipeline inputs
    pairs = [
        {"text": query, "text_pair": chunk["text"]} 
        for chunk in retrieved_chunks
    ]

    try:
        # 3. Use your target BGE Reranker model via text_classification
        api_results = client.text_classification(
            text=pairs, 
            model="BAAI/bge-reranker-v2-m3"
        )

        reranked = []
        # Match each original chunk to its corresponding API score output
        for chunk, api_res in zip(retrieved_chunks, api_results):
            # The API returns a list of objects; safely handle dictionary or object types
            score = (
                api_res.get("score", 0.0)
                if isinstance(api_res, dict)
                else getattr(api_res, "score", 0.0)
            )

            reranked.append({
                "chunk": chunk, 
                "rerank_score": float(score)
            })

        # 4. Sort results by the highest matching score descending
        reranked.sort(key=lambda x: x["rerank_score"], reverse=True)

        print("\nRAW RETRIEVED CHUNKS:\n", retrieved_chunks)
        print("\nFINAL RERANKED RESULTS:\n", reranked)

        return reranked[:top_k]

    except Exception as e:
        raise RuntimeError(
            f"Failed to execute BGE cross-encoder reranking via Hub Client: {e}"
        )
