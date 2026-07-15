from rank_bm25 import BM25Okapi


class BM25Retriever:

    def __init__(self, chunks):

        self.chunks = chunks

        tokenized_chunks = [
            chunk["text"].split()
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(tokenized_chunks)

    def search(
        self,
        query: str,
        top_k: int = 5
    ):
        MIN_BM25_SCORE = 0.1

        tokenized_query = query.split()

        scores = self.bm25.get_scores(
            tokenized_query
        )

        scored_results = list(
            zip(self.chunks, scores)
        )

        scored_results.sort(
            key=lambda x: x[1],
            reverse=True
        )

        filtered_results = [
            (chunk, score)
            for chunk, score in scored_results
            if score > MIN_BM25_SCORE
            ]

        return filtered_results[:top_k]