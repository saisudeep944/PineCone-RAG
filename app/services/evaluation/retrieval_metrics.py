def precision_at_k(
    retrieved_chunks,
    relevant_chunk_ids,
    k
):

    retrieved_top_k = (
        retrieved_chunks[:k]
    )

    retrieved_ids = [
        chunk["chunk_id"]
        for chunk in retrieved_top_k
    ]

    relevant_retrieved = sum(

        1
        for chunk_id in retrieved_ids

        if chunk_id in relevant_chunk_ids
    )

    precision = (
        relevant_retrieved / k
    )

    return precision

def mean_reciprocal_rank(
    retrieved_chunks,
    relevant_chunk_ids
):

    for rank, chunk in enumerate(
        retrieved_chunks,
        start=1
    ):

        if (
            chunk["chunk_id"]
            in relevant_chunk_ids
        ):

            return 1 / rank

    return 0