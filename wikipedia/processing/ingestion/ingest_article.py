"""Generation-aware, resumable ingestion of one offline Wikipedia article."""

import sys
import uuid
from libzim.reader import Archive
from bs4 import BeautifulSoup

from test_chunking import (
    ZIM_PATH,
    MAX_CHARS,
    NON_PROSE_SELECTORS,
    article_html,
    remove_excluded_sections,
    eligible_records,
    make_chunks,
)
from batch_embeddings import embed_batch, BATCH_SIZE
from qdrant_batch import upload_batch
from ingestion_target import ACTIVE_COLLECTION
from qdrant_cleanup import remove_stale_chunks, remove_article_chunks
import ingestion_progress as progress
from ingestion_config import configuration_id
from article_generations import (
    register_generation,
    validate_generation,
    fail_generation,
    publish_generation,
    get_published_generation,
)


class ConfirmedUnsupportedArticle(Exception):
    """Article content is explicitly confirmed to be unsupported."""


def ingest_article(title):
    """
    Complete generation-aware ingestion for a Wikipedia article.
    
    Returns the processing status ("completed", "excluded", or "skipped").
    """
    print(f"Opening Wikipedia article: {title}")

    archive = Archive(ZIM_PATH)
    entry = archive.get_entry_by_title(title)

    while entry.is_redirect:
        entry = entry.get_redirect_entry()

    article_path = entry.path

    config_id = configuration_id()
    
    # Register the article first to ensure it's tracked
    progress.register_article(article_path, title, config_id)
    
    if progress.is_completed(article_path, config_id):
        print(f"SKIPPED: {title} already completed")
        return "skipped"

    if progress.is_excluded(article_path, config_id):
        print(f"EXCLUDED: {title} previously excluded")
        return "excluded"

    # Generate a unique generation ID for this ingestion run
    generation_id = str(uuid.uuid4())
    
    # Register the new generation
    register_generation(article_path, generation_id, config_id)
    
    # Mark article as processing
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
        expected_chunk_count = len(chunks)
        
        # Process in batches
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
                generation_id=generation_id,
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
            generation_id=generation_id,
        )

        print(f"Stale chunks removed: {stale_removed}")

        # Validate the generation after successful upload
        validate_generation(
            article_path,
            generation_id,
            config_id,
            expected_chunk_count,
            total_uploaded
        )

        # Atomically publish the validated generation  
        with progress.connect() as connection:
            published = get_published_generation(connection, article_path, config_id)
            
            # For first publication, expected_revision is None
            if published is None:
                expected_revision = None
            else:
                expected_revision = published["revision"]
                
            publish_generation(
                connection,
                article_path,
                generation_id,
                config_id,
                expected_revision
            )

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
                generation_id=generation_id,
            )

            # Mark the generation as failed
            fail_generation(article_path, generation_id, config_id)
            
            # Also update the article status
            progress.exclude_article(
                article_path,
                exclusion_reason,
                config_id,
            )

        except Exception as cleanup_error:
            try:
                # Mark generation as failed even if cleanup fails
                fail_generation(article_path, generation_id, config_id)
            except:
                pass
                
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
        # Mark generation as failed and article as failed
        try:
            fail_generation(article_path, generation_id, config_id)
        except:
            pass
            
        progress.fail_article(article_path, error, config_id)
        print(f"INGESTION FAILED: {error}")
        raise


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python ingest_article.py "Article Title"')
        raise SystemExit(2)

    ingest_article(sys.argv[1])