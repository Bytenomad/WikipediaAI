"""Checkpoint-aware Wikipedia article enumeration."""

from enumerate_articles import enumerate_articles
from enumeration_checkpoint import get_checkpoint


def resumable_articles(archive, checkpoint_name, configuration_id):
    """Yield (position, article) after a validated checkpoint."""

    checkpoint = get_checkpoint(checkpoint_name, configuration_id)

    if checkpoint is None:
        for position, article in enumerate(
            enumerate_articles(archive), start=1
        ):
            yield position, article
        return

    checkpoint_position = checkpoint["articles_scanned"]

    if checkpoint_position < 1:
        raise ValueError("Invalid checkpoint position")

    checkpoint_found = False

    for position, article in enumerate(
        enumerate_articles(archive), start=1
    ):
        if position < checkpoint_position:
            continue

        if position == checkpoint_position:
            if (
                article["title"] != checkpoint["last_article_title"]
                or article["article_path"] != checkpoint["last_article_path"]
            ):
                raise RuntimeError(
                    "Checkpoint article mismatch at position "
                    f"{checkpoint_position}"
                )

            checkpoint_found = True
            continue

        yield position, article

    if not checkpoint_found:
        raise RuntimeError(
            "Checkpoint position "
            f"{checkpoint_position} was not found in the archive"
        )