"""Incremental Qdrant uploads for offline Wikipedia ingestion."""

import uuid

from qdrant_client import QdrantClient, models
from urllib.parse import quote

from wikipedia_ai.ingestion.target import ACTIVE_COLLECTION, TEST_COLLECTION, validate_ingestion_collection
VECTOR_DIMENSIONS = 768
BATCH_SIZE = 32


def upload_batch(article_title, article_path, chunks, vectors,
                 collection=TEST_COLLECTION, configuration_id=None,
                 generation_id=None):
    """Upload one batch of article chunks to Qdrant."""

    validate_ingestion_collection(collection)

    if collection == ACTIVE_COLLECTION and (
        not isinstance(generation_id, str)
        or not generation_id.strip()
    ):
        raise ValueError(
            "Generation ID required for staging uploads"
        )

    if not isinstance(configuration_id, str) or not configuration_id.strip():
        raise ValueError("configuration_id is required")

    if generation_id is not None:
        if not isinstance(generation_id, str) or not generation_id.strip():
            raise ValueError("A nonempty generation_id is required")

    if not chunks or len(chunks) != len(vectors):
        raise ValueError("Chunks and vectors must have equal nonzero lengths")

    if len(chunks) > BATCH_SIZE:
        raise ValueError(f"Batch exceeds {BATCH_SIZE} chunks")

    points = []

    for chunk, vector in zip(chunks, vectors):
        if len(vector) != VECTOR_DIMENSIONS:
            raise ValueError("Incorrect embedding dimensions")

        index = int(chunk["chunk_index"])

        if generation_id is None:
            identity = (
                f"wikipedia-v4:{configuration_id}:{article_path}:{index}"
            )
        else:
            identity = (
                f"wikipedia-v5:{configuration_id}:{article_path}:"
                f"{generation_id}:{index}"
            )

        point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, identity))

        payload = {
            "title": article_title,
            "article_path": article_path,
            "section": chunk["section"],
            "chunk_index": index,
            "text": chunk["text"],
            "source": "wikipedia",
            "embedding_model": "nomic-embed-text",
            "configuration_id": configuration_id,
            "kiwix_url": (
                "http://127.0.0.1:8080/content/"
                "wikipedia_en_all_maxi_2026-08/"
                + quote(article_path, safe="/")
            ),
        }

        if generation_id is not None:
            payload["generation_id"] = generation_id

        points.append(models.PointStruct(
            id=point_id,
            vector=vector,
            payload=payload,
        ))

    client = QdrantClient(url="http://127.0.0.1:6333")

    client.upsert(
        collection_name=collection,
        points=points,
        wait=True,
    )

    return len(points)