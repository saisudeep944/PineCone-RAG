def reciprocal_rank_fusion(
    vector_results,
    bm25_results,
    k: int = 60
):

    fused_scores = {}

    # Vector results
    for rank, result in enumerate(vector_results):

        chunk_id = result["chunk_id"]

        score = 1 / (k + rank + 1)

        fused_scores[chunk_id] = (
            fused_scores.get(chunk_id, 0)
            + score
        )

    # BM25 results
    for rank, (chunk, _) in enumerate(bm25_results):

        chunk_id = chunk["chunk_id"]

        score = 1 / (k + rank + 1)

        fused_scores[chunk_id] = (
            fused_scores.get(chunk_id, 0)
            + score
        )

    ranked_chunk_ids = sorted(
        fused_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked_chunk_ids