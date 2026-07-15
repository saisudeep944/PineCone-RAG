from app.services.retrieval_service import (
    retrieve_documents
)

from app.services.hybrid.reranker_service import (
    rerank_results
)

from app.services.llm.prompt_builder import (
    build_rag_prompt
)

query = """
What does the document say about AI?
"""

# Retrieval
results = retrieve_documents(

    query=query,

    namespace="AI_Medical_Device",

    top_k=5
)

# Reranking
reranked = rerank_results(

    query=query,

    retrieved_chunks=results,

    top_k=3
)

reranked_chunks = [

    item["chunk"]
    for item in reranked
]

# Prompt Construction
prompt = build_rag_prompt(

    query=query,

    retrieved_chunks=
    reranked_chunks
)

print("\nRAG PROMPT:\n")

print(prompt)