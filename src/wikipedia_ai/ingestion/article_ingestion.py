"""Resumable, batched ingestion of one offline Wikipedia article."""

import sys
from libzim.reader import Archive
from bs4 import BeautifulSoup

from wikipedia_ai.ingestion.chunking import (
    ZIM_PATH,
    MAX_CHARS,
    NON_PROSE_SELECTORS,
    article_html,
    remove_excluded_sections,
    eligible_records,
    make_chunks,
)
from wikipedia_ai.ingestion.batch_embeddings import embed_batch, BATCH_SIZE
from wikipedia_ai.ingestion.qdrant_batch import upload_batch
from wikipedia_ai.ingestion.target import ACTIVE_COLLECTION
from wikipedia_ai.ingestion.cleanup import remove_stale_chunks, remove_article_chunks
import wikipedia_ai.ingestion.progress_tracking as progress
from wikipedia_ai.ingestion.config import configuration_id


class ConfirmedUnsupportedArticle(Exception):
    """Article content is explicitly confirmed to be unsupported."""


def ingest_article(title):
    raise RuntimeError(
        "Legacy article ingestion is disabled until generation-aware "
        "publication and recovery are integrated and verified."
    )

    print(f"Opening Wikipedia article: {title}")

    archive = Archive(ZIM_PATH)
    entry = archive.get_entry_by_title(title)

    while entry.is_redirect:
        entry = entry.get_redirect_entry()

    article_path = entry.path

    config_id = configuration_id()
    progress.register_article(article_path, title, config_id)

    if progress.is_completed(article_path, config_id):
        print(f"SKIPPED: {title} already completed")
        return "skipped"

    if progress.is_excluded(article_path, config_id):
        print(f"EXCLUDED: {title} previously excluded")
        return "excluded"

    progress.start_article(article_path, config_id)

    try:
        soup = BeautifulSoup(article_html(archive, title), "lxml")
        content = soup.select_one(".mw-parser-output")

        if content is None:
            raise RuntimeError("Article content not found")

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

        print(f"Article: {title}")
        print(f"Chunks: {len(chunks)}")

        if not chunks:
            raise RuntimeError("Article produced no chunks")

        total_uploaded = 0

        for start in range(0, len(chunks), BATCH_SIZE):
            batch = chunks[start:start + BATCH_SIZE]

            indexed_chunks = [
                {
                    "chunk_index": start + offset,
                    "section": chunk["section"],
                    "text": chunk["text"],
                }
                for offset, chunk in enumerate(batch)
            ]

            vectors = embed_batch(
                [chunk["text"] for chunk in indexed_chunks]
            )

            uploaded = upload_batch(
                title,
                article_path,
                indexed_chunks,
                vectors,
                collection=ACTIVE_COLLECTION,
                configuration_id=config_id,
            )

            total_uploaded += uploaded

            print(
                f"Uploaded {total_uploaded}/{len(chunks)} chunks"
            )

        # Remove obsolete chunks only after all new chunks
        # have been successfully uploaded.
        stale_removed = remove_stale_chunks(
            article_path,
            len(chunks),
            ACTIVE_COLLECTION,
            config_id,
        )

        print(f"Stale chunks removed: {stale_removed}")

        progress.complete_article(article_path, len(chunks), config_id)
        print("INGESTION COMPLETE")        
        print("Article:", title)
        print("Chunks uploaded:", total_uploaded)
        print("Collection:", ACTIVE_COLLECTION)
        return "completed"

    except ConfirmedUnsupportedArticle as reason:
        try:
            exclusion_reason = str(reason).strip()

            if not exclusion_reason:
                raise ValueError(
                    "A nonempty exclusion reason is required"
                )

            removed = remove_article_chunks(
                article_path,
                ACTIVE_COLLECTION,
                config_id,
            )

            progress.exclude_article(
                article_path,
                exclusion_reason,
                config_id,
            )

        except Exception as cleanup_error:
            progress.fail_article(
                article_path,
                cleanup_error,
                config_id,
            )
            print(f"EXCLUSION CLEANUP FAILED: {cleanup_error}")
            raise

        print(f"EXCLUDED: {title}")
        print(f"Reason: {reason}")
        print(f"Vectors removed: {removed}")
        return "excluded"

    except Exception as error:
        progress.fail_article(article_path, error, config_id)
        print(f"INGESTION FAILED: {error}")
        raise


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python ingest_article.py "Article Title"')
        raise SystemExit(2)

    ingest_article(sys.argv[1])