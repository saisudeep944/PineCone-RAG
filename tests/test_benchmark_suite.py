from statistics import mean

from evaluation_data.benchmark_queries import (
    benchmark_queries
)

from app.services.retrieval_service import (
    retrieve_documents
)

from app.services.hybrid.reranker_service import (
    rerank_results
)

from app.services.evaluation.retrieval_metrics import (
    mean_reciprocal_rank
)

raw_mrr_scores = []

reranked_mrr_scores = []

for item in benchmark_queries:

    query = item["query"]

    relevant_chunk_ids = item[
        "relevant_chunk_ids"
    ]

    # ============================
    # Raw Retrieval
    # ============================

    raw_results = retrieve_documents(

        query=query,

        namespace="AI_Medical_Device",

        top_k=5
    )

    raw_mrr = mean_reciprocal_rank(

        retrieved_chunks=
        raw_results,

        relevant_chunk_ids=
        relevant_chunk_ids
    )

    raw_mrr_scores.append(
        raw_mrr
    )

    # ============================
    # Reranked Retrieval
    # ============================

    reranked = rerank_results(

        query=query,

        retrieved_chunks=
        raw_results,

        top_k=5
    )

    reranked_chunks = [

        result["chunk"]
        for result in reranked
    ]

    reranked_mrr = (
        mean_reciprocal_rank(

            retrieved_chunks=
            reranked_chunks,

            relevant_chunk_ids=
            relevant_chunk_ids
        )
    )

    reranked_mrr_scores.append(
        reranked_mrr
    )

    # ============================
    # Query-Level Output
    # ============================

    print("=" * 80)

    print(f"QUERY: {query}")

    print(f"RAW MRR: {raw_mrr}")

    print(
        f"RERANKED MRR: "
        f"{reranked_mrr}"
    )

# ====================================
# Aggregate Metrics
# ====================================

print("\nFINAL BENCHMARK RESULTS:\n")

print(
    f"Average Raw MRR: "
    f"{mean(raw_mrr_scores)}"
)

print(
    f"Average Reranked MRR: "
    f"{mean(reranked_mrr_scores)}"
)

print(
    f"Overall MRR Lift: "
    f"{mean(reranked_mrr_scores) - mean(raw_mrr_scores)}"
)