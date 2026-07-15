def validate_retrieval_confidence(

    retrieved_chunks,

    min_vector_score=0.35
):

    if not retrieved_chunks:

        return False

    top_score = retrieved_chunks[0].get(
        "vector_score",
        0
    )

    if top_score < min_vector_score:

        return False

    return True