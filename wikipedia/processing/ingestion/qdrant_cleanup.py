"""Remove obsolete Qdrant chunks after successful article reindexing."""

from qdrant_client import QdrantClient, models
from ingestion_target import validate_ingestion_collection

QDRANT_URL = "http://127.0.0.1:6333"


def remove_stale_chunks(article_path, valid_chunk_count, collection, configuration_id):
    """Delete chunks whose indices exceed the article's current range."""

    if not article_path:
        raise ValueError("article_path must not be empty")

    if not isinstance(configuration_id, str) or not configuration_id:
        raise ValueError("configuration_id is required")

    if valid_chunk_count <= 0:
        raise ValueError("valid_chunk_count must be positive")

    validate_ingestion_collection(collection)

    client = QdrantClient(url=QDRANT_URL)

    article_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="article_path",
                match=models.MatchValue(value=article_path),
            ),
            models.FieldCondition(
                key="chunk_index",
                range=models.Range(gte=valid_chunk_count),
            ),
            models.FieldCondition(
                key="configuration_id",
                match=models.MatchValue(value=configuration_id),
            ),
        ]
    )

    stale_count = client.count(
        collection_name=collection,
        count_filter=article_filter,
        exact=True,
    ).count

    if stale_count:
        client.delete(
            collection_name=collection,
            points_selector=models.FilterSelector(
                filter=article_filter,
            ),
            wait=True,
        )

    return stale_count


def remove_article_chunks(article_path, collection, configuration_id):
    """Remove all vectors for one article and configuration."""

    if not isinstance(article_path, str) or not article_path.strip():
        raise ValueError("A nonempty article_path is required")

    if not isinstance(configuration_id, str) or not configuration_id.strip():
        raise ValueError("A nonempty configuration_id is required")

    validate_ingestion_collection(collection)

    article_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="article_path",
                match=models.MatchValue(value=article_path),
            ),
            models.FieldCondition(
                key="configuration_id",
                match=models.MatchValue(value=configuration_id),
            ),
        ]
    )

    client = QdrantClient(url=QDRANT_URL)

    before = client.count(
        collection_name=collection,
        count_filter=article_filter,
        exact=True,
    ).count

    if before:
        client.delete(
            collection_name=collection,
            points_selector=models.FilterSelector(
                filter=article_filter,
            ),
            wait=True,
        )

    after = client.count(
        collection_name=collection,
        count_filter=article_filter,
        exact=True,
    ).count

    if after != 0:
        raise RuntimeError(
            f"Article vector cleanup incomplete: {after} remain"
        )

    return before


def remove_failed_generation(
    connection,
    article_path,
    generation_id,
    configuration_id,
    collection,
):
    """Remove vectors belonging to one failed, unpublished generation.

    Requires every publisher to use the same SQLite locking protocol.
    Qdrant deletion is not transactional with SQLite.
    """
    from article_generations import get_published_generation

    for name, value in (
        ("article_path", article_path),
        ("generation_id", generation_id),
        ("configuration_id", configuration_id),
    ):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Nonempty {name} required")

    validate_ingestion_collection(collection)

    if connection.in_transaction:
        raise RuntimeError(
            "Cleanup requires its own SQLite transaction"
        )

    connection.execute("BEGIN IMMEDIATE")

    try:
        record = connection.execute(
            """
            SELECT status
            FROM article_generations
            WHERE configuration_id = ?
              AND article_path = ?
              AND generation_id = ?
            """,
            (configuration_id, article_path, generation_id),
        ).fetchone()

        if record is None or record[0] != "failed":
            raise RuntimeError(
                "Only failed generations may be cleaned up"
            )

        published = get_published_generation(
            connection,
            article_path,
            configuration_id,
        )

        if (
            published is not None
            and published["generation_id"] == generation_id
        ):
            raise RuntimeError(
                "Cannot delete a published generation"
            )

        generation_filter = models.Filter(must=[
            models.FieldCondition(
                key="configuration_id",
                match=models.MatchValue(
                    value=configuration_id
                ),
            ),
            models.FieldCondition(
                key="article_path",
                match=models.MatchValue(
                    value=article_path
                ),
            ),
            models.FieldCondition(
                key="generation_id",
                match=models.MatchValue(
                    value=generation_id
                ),
            ),
        ])

        client = QdrantClient(url=QDRANT_URL)

        before = client.count(
            collection_name=collection,
            count_filter=generation_filter,
            exact=True,
        ).count

        if before:
            client.delete(
                collection_name=collection,
                points_selector=models.FilterSelector(
                    filter=generation_filter
                ),
                wait=True,
            )

        after = client.count(
            collection_name=collection,
            count_filter=generation_filter,
            exact=True,
        ).count

        if after != 0:
            raise RuntimeError(
                f"Generation cleanup incomplete: {after} remain"
            )

        connection.execute("COMMIT")
        return before

    except BaseException:
        if connection.in_transaction:
            connection.execute("ROLLBACK")
        raise
