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

# ====================================
# Quality Thresholds
# ====================================

MIN_ACCEPTABLE_MRR = 0.55

# ====================================
# Evaluation
# ====================================

mrr_scores = []

for item in benchmark_queries:

    query = item["query"]

    relevant_chunk_ids = item[
        "relevant_chunk_ids"
    ]

    results = retrieve_documents(

        query=query,

        namespace="AI_Medical_Device",

        top_k=5
    )

    reranked = rerank_results(

        query=query,

        retrieved_chunks=results,

        top_k=5
    )

    reranked_chunks = [

        result["chunk"]
        for result in reranked
    ]

    mrr = mean_reciprocal_rank(

        retrieved_chunks=
        reranked_chunks,

        relevant_chunk_ids=
        relevant_chunk_ids
    )

    mrr_scores.append(mrr)

# ====================================
# Aggregate Quality
# ====================================

average_mrr = mean(mrr_scores)

print("\nAVERAGE MRR:\n")

print(average_mrr)

# ====================================
# Regression Validation
# ====================================

assert (
    average_mrr
    >=
    MIN_ACCEPTABLE_MRR
), (

    f"Retrieval regression detected! "
    f"MRR dropped below "
    f"{MIN_ACCEPTABLE_MRR}"
)

print("\nRETRIEVAL QUALITY PASSED\n")