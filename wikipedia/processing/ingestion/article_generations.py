"""Generation tracking for Wikipedia article ingestion."""

import sqlite3

import ingestion_progress as progress


def register_generation(
    article_path: str,
    generation_id: str,
    configuration_id: str,
) -> None:
    """Register a new, unpublished article generation."""

    if not isinstance(article_path, str) or not article_path.strip():
        raise ValueError("A nonempty article_path is required")

    if not isinstance(generation_id, str) or not generation_id.strip():
        raise ValueError("A nonempty generation_id is required")

    configuration_id = progress.validate_configuration_id(
        configuration_id
    )

    with progress.connect() as connection:
        article = connection.execute("""
            SELECT 1
            FROM articles
            WHERE configuration_id = ?
              AND article_path = ?
        """, (configuration_id, article_path)).fetchone()

        if article is None:
            raise ValueError(
                "Cannot register a generation for an unknown article"
            )

        connection.execute("""
            INSERT INTO article_generations (
                configuration_id,
                article_path,
                generation_id,
                status,
                chunk_count
            )
            VALUES (?, ?, ?, 'processing', 0)
        """, (
            configuration_id,
            article_path,
            generation_id,
        ))


def validate_generation(
    article_path: str,
    generation_id: str,
    configuration_id: str,
    expected_chunks: int,
    verified_chunks: int,
) -> None:
    """Mark a generation validated after external chunk verification."""

    if not isinstance(article_path, str) or not article_path.strip():
        raise ValueError("A nonempty article_path is required")

    if not isinstance(generation_id, str) or not generation_id.strip():
        raise ValueError("A nonempty generation_id is required")

    configuration_id = progress.validate_configuration_id(
        configuration_id
    )

    if type(expected_chunks) is not int or expected_chunks <= 0:
        raise ValueError("expected_chunks must be a positive integer")

    if type(verified_chunks) is not int or verified_chunks <= 0:
        raise ValueError("verified_chunks must be a positive integer")

    if expected_chunks != verified_chunks:
        raise ValueError(
            "Expected and verified chunk counts do not match"
        )

    with progress.connect() as connection:
        cursor = connection.execute("""
            UPDATE article_generations
            SET status = 'validated',
                chunk_count = ?
            WHERE configuration_id = ?
              AND article_path = ?
              AND generation_id = ?
              AND status = 'processing'
        """, (
            verified_chunks,
            configuration_id,
            article_path,
            generation_id,
        ))

        if cursor.rowcount != 1:
            raise RuntimeError(
                "Generation not found or not in processing state"
            )


def fail_generation(
    article_path: str,
    generation_id: str,
    configuration_id: str,
) -> None:
    """Mark an unpublished processing generation as failed."""

    if not isinstance(article_path, str) or not article_path.strip():
        raise ValueError("A nonempty article_path is required")

    if not isinstance(generation_id, str) or not generation_id.strip():
        raise ValueError("A nonempty generation_id is required")

    configuration_id = progress.validate_configuration_id(
        configuration_id
    )

    with progress.connect() as connection:
        cursor = connection.execute("""
            UPDATE article_generations
            SET status = 'failed'
            WHERE configuration_id = ?
              AND article_path = ?
              AND generation_id = ?
              AND status = 'processing'
              AND NOT EXISTS (
                  SELECT 1
                  FROM published_generations AS published
                  WHERE published.configuration_id =
                        article_generations.configuration_id
                    AND published.article_path =
                        article_generations.article_path
                    AND published.generation_id =
                        article_generations.generation_id
              )
        """, (
            configuration_id,
            article_path,
            generation_id,
        ))

        if cursor.rowcount != 1:
            raise RuntimeError(
                "Generation not found, not processing, "
                "or already published"
            )


def publish_generation(
    connection: sqlite3.Connection,
    article_path: str,
    generation_id: str,
    configuration_id: str,
    expected_revision: int | None,
) -> None:
    """Atomically publish a validated generation using revision-based CAS."""

    for name, value in (
        ("article_path", article_path),
        ("generation_id", generation_id),
        ("configuration_id", configuration_id),
    ):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"A nonempty {name} is required")

    if expected_revision is not None and (
        isinstance(expected_revision, bool)
        or not isinstance(expected_revision, int)
        or expected_revision < 1
    ):
        raise ValueError(
            "expected_revision must be None or a positive integer"
        )

    if connection.in_transaction:
        raise RuntimeError(
            "Publication requires a connection without an active transaction"
        )

    if connection.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
        raise RuntimeError(
            "Publication requires SQLite foreign-key enforcement"
        )

    connection.execute("BEGIN IMMEDIATE")

    try:
        record = connection.execute("""
            SELECT status, chunk_count
            FROM article_generations
            WHERE configuration_id = ?
              AND article_path = ?
              AND generation_id = ?
        """, (
            configuration_id,
            article_path,
            generation_id,
        )).fetchone()

        if (
            record is None
            or record[0] != "validated"
            or record[1] <= 0
        ):
            raise RuntimeError(
                "Generation does not exist or is not publishable"
            )

        if expected_revision is None:
            cursor = connection.execute("""
                INSERT INTO published_generations (
                    configuration_id,
                    article_path,
                    generation_id,
                    revision
                )
                VALUES (?, ?, ?, 1)
                ON CONFLICT(configuration_id, article_path)
                DO NOTHING
            """, (
                configuration_id,
                article_path,
                generation_id,
            ))
        else:
            cursor = connection.execute("""
                UPDATE published_generations
                SET generation_id = ?,
                    revision = revision + 1,
                    published_at = CURRENT_TIMESTAMP
                WHERE configuration_id = ?
                  AND article_path = ?
                  AND revision = ?
            """, (
                generation_id,
                configuration_id,
                article_path,
                expected_revision,
            ))

        if cursor.rowcount != 1:
            raise RuntimeError(
                "Stale publication revision; publication rejected"
            )

        connection.execute("COMMIT")

    except BaseException:
        if connection.in_transaction:
            connection.execute("ROLLBACK")
        raise


def get_published_generation(
    connection: sqlite3.Connection,
    article_path: str,
    configuration_id: str,
) -> dict | None:
    """Return the published generation and revision, or None."""

    for name, value in (
        ("article_path", article_path),
        ("configuration_id", configuration_id),
    ):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"A nonempty {name} is required")

    row = connection.execute("""
        SELECT generation_id, revision
        FROM published_generations
        WHERE configuration_id = ?
          AND article_path = ?
    """, (
        configuration_id,
        article_path,
    )).fetchone()

    if row is None:
        return None

    generation_id, revision = row

    if (
        not isinstance(generation_id, str)
        or not generation_id.strip()
        or type(revision) is not int
        or revision < 1
    ):
        raise RuntimeError(
            "Invalid published-generation record"
        )

    return {
        "generation_id": generation_id,
        "revision": revision,
    }
