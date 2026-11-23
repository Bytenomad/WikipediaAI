
"""Index the Medicine Wikipedia article into Qdrant v2."""

from __future__ import annotations

import os
import sys
import uuid
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from libzim.reader import Archive
from qdrant_client import QdrantClient, models

from test_chunking import (
    ZIM_PATH,
    ARTICLE_TITLE,
    MAX_CHARS,
    NON_PROSE_SELECTORS,
    article_html,
    remove_excluded_sections,
    eligible_records,
    make_chunks,
)

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/embed")
EMBEDDING_MODEL = "nomic-embed-text"
QDRANT_URL = os.environ.get("QDRANT_URL", "http://127.0.0.1:6333")
COLLECTION = "wikipedia_articles_v2"

KIWIX_BASE_URL = (
    "http://127.0.0.1:8080/content/"
    "wikipedia_en_all_maxi_2026-08/"
)


def embed(text: str) -> list[float]:
    response = requests.post(
        OLLAMA_URL,
        json={"model": EMBEDDING_MODEL, "input": text},
        timeout=120,
    )
    response.raise_for_status()
    vector = response.json()["embeddings"][0]

    if len(vector) != 768:
        raise ValueError(
            f"Expected 768 dimensions, got {len(vector)}"
        )

    return vector


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    article_title = sys.argv[1] if len(sys.argv) > 1 else ARTICLE_TITLE
    print("Opening Wikipedia ZIM...")
    archive = Archive(ZIM_PATH)

    entry = archive.get_entry_by_title(article_title)

    while entry.is_redirect:
        entry = entry.get_redirect_entry()

    article_path = entry.path

    print(f"Resolved article path: {article_path}")

    soup = BeautifulSoup(
        article_html(archive, article_title),
        "lxml",
    )

    content = soup.select_one(".mw-parser-output")
    if content is None:
        raise RuntimeError("Wikipedia article content not found")

    remove_excluded_sections(content)

    for node in content.select(NON_PROSE_SELECTORS):
        node.decompose()

    records = eligible_records(content)
    chunks = make_chunks(records, MAX_CHARS)

    original_words = " ".join(
        record["text"] for record in records
    ).split()
    chunk_words = " ".join(
        str(chunk["text"]) for chunk in chunks
    ).split()

    if original_words != chunk_words:
        raise RuntimeError("Content preservation check failed")

    print(f"Article: {article_title}")
    print(f"Validated chunks: {len(chunks)}")

    client = QdrantClient(url=QDRANT_URL)

    if not client.collection_exists(COLLECTION):
        raise RuntimeError(
            f"Qdrant collection does not exist: {COLLECTION}"
        )

    points = []

    for index, chunk in enumerate(chunks):
        section = str(chunk["section"])
        text = str(chunk["text"])

        print(
            f"Embedding {index + 1}/{len(chunks)} "
            f"| {section}"
        )

        vector = embed(text)

        point_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"wikipedia-v2:{article_title}:{index}",
            )
        )

        points.append(
            models.PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "title": article_title,
                    "article_path": article_path,
                    "section": section,
                    "chunk_index": index,
                    "text": text,
                    "source": "wikipedia",
                    "embedding_model": EMBEDDING_MODEL,
                    "kiwix_url": (
                        KIWIX_BASE_URL + quote(article_path, safe="/")
                    ),
                },
            )
        )

    print("Uploading points to Qdrant...")

    client.upsert(
        collection_name=COLLECTION,
        points=points,
        wait=True,
    )

    info = client.get_collection(COLLECTION)

    print()
    print("INDEXING COMPLETE")
    print(f"Article: {article_title}")
    print(f"Chunks uploaded: {len(points)}")
    print(f"Collection points: {info.points_count}")
    print(f"Collection: {COLLECTION}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
