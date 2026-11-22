"""Checkpoint-aware sequential Wikipedia batch ingestion."""

from libzim.reader import Archive

from checkpoint_identity import checkpoint_name
from enumeration_checkpoint import save_verified_checkpoint
from ingestion_config import configuration_id
from ingest_article import ingest_article
from resumable_enumerator import resumable_articles
from test_chunking import ZIM_PATH




def ingest_batch(max_articles=5):
    """Ingest a limited number of articles with checkpoint recovery."""

    if not isinstance(max_articles, int) or isinstance(max_articles, bool):
        raise ValueError("max_articles must be an integer")

    if max_articles < 1:
        raise ValueError("max_articles must be positive")

    config_id = configuration_id()
    active_checkpoint = checkpoint_name(config_id)
    archive = Archive(str(ZIM_PATH))

    completed = 0
    skipped = 0
    excluded = 0

    for position, article in resumable_articles(
        archive,
        active_checkpoint,
        config_id,
    ):
        if completed + skipped + excluded >= max_articles:
            break

        title = article["title"]
        article_path = article["article_path"]

        print(f"\n[{position}] Processing: {title}")

        result = ingest_article(title)

        if result not in ("completed", "skipped", "excluded"):
            raise RuntimeError(
                f"Unexpected ingestion result for {title}: {result!r}"
            )

        save_verified_checkpoint(
            checkpoint_name=active_checkpoint,
            title=title,
            article_path=article_path,
            articles_scanned=position,
            configuration_id=config_id,
            result=result,
        )

        if result == "completed":
            completed += 1
        elif result == "skipped":
            skipped += 1
        elif result == "excluded":
            excluded += 1

    summary = {
        "completed": completed,
        "skipped": skipped,
        "excluded": excluded,
        "handled": completed + skipped + excluded,
    }

    print("\nBATCH INGESTION SUMMARY")
    print("Completed:", completed)
    print("Skipped:", skipped)
    print("Excluded:", excluded)
    print("Handled:", summary["handled"])

    return summary


if __name__ == "__main__":
    raise SystemExit(
        "Direct execution is disabled until batch ingestion safety "
        "tests are complete."
    )
