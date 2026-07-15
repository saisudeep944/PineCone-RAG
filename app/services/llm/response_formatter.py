def format_rag_response(
    answer,
    retrieved_chunks
):

    formatted_sources = []

    for idx, chunk in enumerate(
        retrieved_chunks,
        start=1
    ):

        source = f"""

SOURCE {idx}

File:
{chunk['file_name']}

Chunk Index:
{chunk['chunk_index']}
"""

        formatted_sources.append(
            source
        )

    sources_text = "\n".join(
        formatted_sources
    )

    final_response = f"""

========================
ANSWER
========================

{answer}

========================
SOURCES
========================

{sources_text}
"""

    return final_response