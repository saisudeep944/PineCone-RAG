from sentence_transformers import CrossEncoder


reranker_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_results(
    query,
    retrieved_chunks,
    top_k=5
):

    pairs = [
        (query, chunk["text"])
        for chunk in retrieved_chunks
    ]

    scores = reranker_model.predict(pairs)

    reranked = []

    for chunk, score in zip(
        retrieved_chunks,
        scores
    ):

        reranked.append({
            "chunk": chunk,
            "rerank_score": float(score)
        })

    reranked.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )
    print("\nRAW RETRIEVED CHUNKS:\n")

    print(retrieved_chunks)

    print("\nFINAL RERANKED RESULTS:\n")

    print(reranked)
    return reranked[:top_k]