from datetime import datetime


def build_trace(
    query,
    chunk,
    vector_score=None,
    bm25_score=None,
    fusion_score=None,
    rerank_score=None,
    namespace=None,
    retrieval_stage=None
):

    return {

        "timestamp": str(datetime.utcnow()),

        "query": query,

        "chunk_id": chunk.get(
            "chunk_id"
        ),

        "file_name": chunk.get(
            "file_name"
        ),

        "chunk_index": chunk.get(
            "chunk_index"
        ),

        "namespace": namespace,

        "vector_score": vector_score,

        "bm25_score": bm25_score,

        "fusion_score": fusion_score,

        "rerank_score": rerank_score,

        "retrieval_stage": retrieval_stage,

        "text": chunk.get("text")
    }