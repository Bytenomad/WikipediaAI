"""Configuration-scoped progress tracking for Wikipedia ingestion."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

# Note: This uses a relative path approach, should be configurable in production
DB_PATH = Path(__file__).parent / "ingestion_progress.db"


def validate_configuration_id(configuration_id):
    if not isinstance(configuration_id, str) or not configuration_id.strip():
        raise ValueError("A nonempty configuration_id is required")
    return configuration_id


@contextmanager
def connect():
    connection = sqlite3.connect(DB_PATH, timeout=30)
    try:
        connection.execute("PRAGMA busy_timeout = 30000")
        with connection:
            yield connection
    finally:
        connection.close()


def register_article(article_path, title, configuration_id):
    configuration_id = validate_configuration_id(configuration_id)

    if not article_path or not title:
        raise ValueError("article_path and title are required")

    with connect() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO articles (
                configuration_id, article_path, title
            )
            VALUES (?, ?, ?)
            """,
            (configuration_id, article_path, title),
        )


def get_article(article_path, configuration_id):
    configuration_id = validate_configuration_id(configuration_id)

    with connect() as connection:
        row = connection.execute(
            """
            SELECT article_path, title, status,
                   chunk_count, attempts, last_error,
                   configuration_id
            FROM articles
            WHERE article_path = ?
              AND configuration_id = ?
            """,
            (article_path, configuration_id),
        ).fetchone()

    if row is None:
        return None

    return dict(zip(
        (
            "article_path", "title", "status",
            "chunk_count", "attempts", "last_error",
            "configuration_id",
        ),
        row,
    ))


def start_article(article_path, configuration_id):
    configuration_id = validate_configuration_id(configuration_id)

    with connect() as connection:
        cursor = connection.execute(
            """
            UPDATE articles
            SET status = 'processing',
                chunk_count = 0,
                attempts = attempts + 1,
                last_error = NULL,
                updated_at = CURRENT_TIMESTAMP
            WHERE article_path = ?
              AND configuration_id = ?
              AND status IN ('pending', 'failed', 'processing')
            """,
            (article_path, configuration_id),
        )

        if cursor.rowcount != 1:
            raise RuntimeError(
                "Article could not transition to processing: "
                f"{article_path}"
            )


def complete_article(article_path, chunk_count, configuration_id):
    configuration_id = validate_configuration_id(configuration_id)

    if not isinstance(chunk_count, int) or chunk_count < 0:
        raise ValueError("chunk_count must be a nonnegative integer")

    with connect() as connection:
        cursor = connection.execute(
            """
            UPDATE articles
            SET status = 'completed',
                chunk_count = ?,
                last_error = NULL,
                updated_at = CURRENT_TIMESTAMP
            WHERE article_path = ?
              AND configuration_id = ?
              AND status = 'processing'
            """,
            (chunk_count, article_path, configuration_id),
        )

        if cursor.rowcount != 1:
            raise RuntimeError(
                "Article could not transition to completed: "
                f"{article_path}"
            )


def fail_article(article_path, error, configuration_id):
    configuration_id = validate_configuration_id(configuration_id)

    with connect() as connection:
        cursor = connection.execute(
            """
            UPDATE articles
            SET status = 'failed',
                last_error = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE article_path = ?
              AND configuration_id = ?
              AND status = 'processing'
            """,
            (str(error), article_path, configuration_id),
        )

        if cursor.rowcount != 1:
            raise RuntimeError(
                "Article could not transition to failed: "
                f"{article_path}"
            )


def is_completed(article_path, configuration_id):
    article = get_article(article_path, configuration_id)
    return article is not None and article["status"] == "completed"


def exclude_article(article_path, reason, configuration_id):
    """Mark a processing article as excluded with a recorded reason."""
    configuration_id = validate_configuration_id(configuration_id)

    if not isinstance(article_path, str) or not article_path.strip():
        raise ValueError("A nonempty article_path is required")

    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("A nonempty exclusion reason is required")

    with connect() as connection:
        cursor = connection.execute(
            """
            UPDATE articles
            SET status = 'excluded',
                chunk_count = 0,
                last_error = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE configuration_id = ?
              AND article_path = ?
              AND status = 'processing'
            """,
            (reason.strip(), configuration_id, article_path),
        )

        if cursor.rowcount != 1:
            raise RuntimeError(
                "Cannot exclude article: "
                "article is not in processing state"
            )


def is_excluded(article_path, configuration_id):
    """Return whether this article is excluded for the configuration."""
    configuration_id = validate_configuration_id(configuration_id)

    article = get_article(article_path, configuration_id)

    return (
        article is not None
        and article["status"] == "excluded"
    )