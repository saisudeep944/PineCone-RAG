from app.services.retrieval_service import (
    retrieve_documents
)

from app.services.hybrid.reranker_service import (
    rerank_results
)

from app.services.llm.prompt_builder import (
    build_rag_prompt
)

from app.services.llm.llm_service import (

    generate_answer,

    stream_answer
)

from app.services.llm.query_rewriter import (
    rewrite_query
)

from app.services.session.session_manager import (

    validate_session,

    refresh_session,

    get_session_metadata,

    deactivate_session,

    save_message
)

from app.services.llm.intent_classifier import (
    classify_intent
)

from app.services.llm.conversation_service import (
    generate_conversational_response
)

from app.services.llm.rewrite_classifier import (
    should_rewrite_query
)

import pprint


# =====================================
# Streaming Chat Response
# =====================================

def stream_chat_response(

    session_id,

    user_message
):

    metadata = (
        get_session_metadata(
            session_id
        )
    )

    namespace = metadata[
        "active_namespace"
    ]

    results = retrieve_documents(

        query=user_message,

        namespace=namespace,

        top_k=5
    )

    reranked = rerank_results(

        query=user_message,

        retrieved_chunks=results,

        top_k=3
    )

    prompt = build_rag_prompt(

        query=user_message,

        retrieved_chunks=reranked
    )

    return stream_answer(
        prompt
    )


# =====================================
# Main Chat Pipeline
# =====================================

def process_chat_message(

    session_id,

    user_message
):

    # =====================================
    # Session Validation
    # =====================================

    if not validate_session(
        session_id
    ):

        return {

            "status":
            "error",

            "message":
            "Invalid session"
        }

    refresh_session(
        session_id
    )

    # =====================================
    # Intent Classification
    # =====================================

    intent = classify_intent(
        user_message
    )

    # =====================================
    # Exit Handling
    # =====================================

    if intent == "exit":

        deactivate_session(
            session_id
        )

        return {

            "status":
            "terminated",

            "intent":
            intent,

            "answer":
            "Session terminated.",

            "sources":
            []
        }

    # =====================================
    # Conversational Intents
    # =====================================

    conversational_intents = [

        "gratitude",

        "acknowledgement",

        "greeting",

        "smalltalk"
    ]

    if intent in conversational_intents:

        response = (
            generate_conversational_response(

                user_message=
                user_message,

                intent=intent
            )
        )

        # Save User Message
        save_message(

            session_id,

            "user",

            user_message
        )

        # Save Assistant Response
        save_message(

            session_id,

            "assistant",

            response
        )

        return {

            "status":
            "success",

            "intent":
            intent,

            "answer":
            response,

            "sources":
            []
        }

    # =====================================
    # Query Rewriting
    # =====================================

    rewrite_needed = (
        should_rewrite_query(
            user_message
        )
    )

    if rewrite_needed:

        rewritten_query = rewrite_query(

            session_id,

            user_message
        )

    else:

        rewritten_query = (
            user_message
        )

    # =====================================
    # Namespace Retrieval
    # =====================================

    metadata = (
        get_session_metadata(
            session_id
        )
    )

    namespace = metadata[
        "active_namespace"
    ]

    print("\nACTIVE NAMESPACE:\n")

    print(namespace)

    results = retrieve_documents(

        query=rewritten_query,

        namespace=namespace,

        top_k=5
    )

    # =====================================
    # Reranking
    # =====================================

    reranked = rerank_results(

        query=rewritten_query,

        retrieved_chunks=results,

        top_k=3
    )

    print("\nRERANKED RESULTS:\n")

    print(reranked)

    print("\nFIRST RERANKED ITEM:\n")

    if reranked:

        pprint.pprint(reranked[0])

    # =====================================
    # Prompt Construction
    # =====================================

    prompt = build_rag_prompt(

        query=rewritten_query,

        retrieved_chunks=reranked
    )

    # =====================================
    # Grounded Generation
    # =====================================

    answer = generate_answer(
        prompt
    )

    # =====================================
    # Save Conversation
    # =====================================

    save_message(

        session_id,

        "user",

        user_message
    )

    save_message(

        session_id,

        "assistant",

        answer
    )

    # =====================================
    # Structured Sources
    # =====================================

    structured_sources = []

    for item in reranked:

        chunk = item["chunk"]

        structured_sources.append({

            "file_name":
            chunk["file_name"],

            "chunk_index":
            chunk["chunk_index"],

            "rerank_score":
            item["rerank_score"],

            "text":
            chunk["text"]
        })

    return {

        "status":
        "success",

        "intent":
        intent,

        "rewritten_query":
        rewritten_query,

        "answer":
        answer,

        "sources":
        structured_sources
    }


# =====================================
# Structured Streaming Response
# =====================================

def stream_structured_response(
    session_id,
    user_message
):
    """
    Streams response as newline-delimited JSON.
    Each event has: type, content, metadata
    Streams word-by-word for smooth real-time display.
    """

    # Get complete response
    response = process_chat_message(
        session_id,
        user_message
    )

    # Stream answer tokens - word by word
    answer = response.get("answer", "")
    
    # Simple word split - preserve everything
    words = answer.split()
    
    for word in words:
        yield {
            "type": "token",
            "content": word + " "
        }

    # Send metadata after stream
    yield {
        "type": "metadata",
        "status": response.get("status"),
        "intent": response.get("intent"),
        "sources": response.get("sources", [])
    }

    # Signal completion
    yield {
        "type": "complete"
    }