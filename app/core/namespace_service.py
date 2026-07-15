from app.core.pinecone_client import (
    index
)


def namespace_exists(
    namespace
):

    stats = (
        index.describe_index_stats()
    )

    namespaces = stats.get(
        "namespaces",
        {}
    )

    return namespace in namespaces
def list_namespaces():

    stats = (
        index.describe_index_stats()
    )

    namespaces = stats.get(
        "namespaces",
        {}
    )

    return list(
        namespaces.keys()
    )    