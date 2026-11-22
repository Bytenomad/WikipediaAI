"""Configuration-aware checkpoints for Wikipedia enumeration."""

import ingestion_progress as progress


def validate_configuration_id(configuration_id):
    if not isinstance(configuration_id, str) or not configuration_id.strip():
        raise ValueError("A nonempty configuration_id is required")


def get_checkpoint(checkpoint_name, configuration_id):
    """Retrieve a checkpoint only when its configuration matches."""

    if not checkpoint_name:
        raise ValueError("checkpoint_name is required")

    validate_configuration_id(configuration_id)

    with progress.connect() as connection:
        row = connection.execute(
            """
            SELECT checkpoint_name, last_article_title,
                   last_article_path, articles_scanned,
                   updated_at, configuration_id
            FROM enumeration_checkpoints
            WHERE checkpoint_name = ?
            """,
            (checkpoint_name,),
        ).fetchone()

    if row is None:
        return None

    checkpoint = dict(zip(
        (
            "checkpoint_name",
            "last_article_title",
            "last_article_path",
            "articles_scanned",
            "updated_at",
            "configuration_id",
        ),
        row,
    ))

    if checkpoint["configuration_id"] != configuration_id:
        raise ValueError(
            "Checkpoint configuration mismatch or legacy checkpoint"
        )

    return checkpoint


def save_checkpoint(
    checkpoint_name,
    title,
    article_path,
    articles_scanned,
    configuration_id,
):
    """Save a checkpoint without changing its configuration or regressing."""

    if not checkpoint_name or not title or not article_path:
        raise ValueError("Checkpoint name, title and path are required")

    validate_configuration_id(configuration_id)

    if not isinstance(articles_scanned, int) or articles_scanned < 0:
        raise ValueError("articles_scanned must be a nonnegative integer")

    with progress.connect() as connection:
        existing = connection.execute(
            """
            SELECT configuration_id
            FROM enumeration_checkpoints
            WHERE checkpoint_name = ?
            """,
            (checkpoint_name,),
        ).fetchone()

        if existing is not None and existing[0] != configuration_id:
            raise ValueError(
                "Checkpoint configuration mismatch or legacy checkpoint"
            )

        connection.execute(
            """
            INSERT INTO enumeration_checkpoints (
                checkpoint_name,
                last_article_title,
                last_article_path,
                articles_scanned,
                configuration_id
            )
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(checkpoint_name) DO UPDATE SET
                last_article_title = excluded.last_article_title,
                last_article_path = excluded.last_article_path,
                articles_scanned = excluded.articles_scanned,
                updated_at = CURRENT_TIMESTAMP
            WHERE enumeration_checkpoints.configuration_id =
                  excluded.configuration_id
              AND excluded.articles_scanned >
                  enumeration_checkpoints.articles_scanned
            """,
            (
                checkpoint_name,
                title,
                article_path,
                articles_scanned,
                configuration_id,
            ),
        )

def save_verified_checkpoint(
    checkpoint_name,
    title,
    article_path,
    articles_scanned,
    configuration_id,
    result,
):
    """Advance only after verifying article publication or exclusion."""

    if not all(
        isinstance(value, str) and value.strip()
        for value in (
            checkpoint_name, title, article_path, configuration_id
        )
    ):
        raise ValueError("Invalid checkpoint identity")

    if (
        not isinstance(articles_scanned, int)
        or isinstance(articles_scanned, bool)
        or articles_scanned < 1
    ):
        raise ValueError("Invalid checkpoint position")

    if result not in ("completed", "skipped", "excluded"):
        raise ValueError("Invalid ingestion result")

    with progress.connect() as connection:
        if connection.in_transaction:
            raise RuntimeError("Unexpected active transaction")

        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("BEGIN IMMEDIATE")

        try:
            previous = connection.execute("""
                SELECT configuration_id, articles_scanned
                FROM enumeration_checkpoints
                WHERE checkpoint_name = ?
            """, (checkpoint_name,)).fetchone()

            if previous is not None and previous[0] != configuration_id:
                raise RuntimeError("Checkpoint configuration mismatch")

            expected = 1 if previous is None else previous[1] + 1

            if articles_scanned != expected:
                raise RuntimeError(
                    "Checkpoint position mismatch: "
                    f"expected {expected}, received {articles_scanned}"
                )

            article = connection.execute("""
                SELECT status
                FROM articles
                WHERE configuration_id = ?
                  AND article_path = ?
            """, (configuration_id, article_path)).fetchone()

            if article is None:
                raise RuntimeError("Article not registered")

            pointer = connection.execute("""
                SELECT generation_id
                FROM published_generations
                WHERE configuration_id = ?
                  AND article_path = ?
            """, (configuration_id, article_path)).fetchone()

            if result == "excluded":
                eligible = (
                    article[0] == "excluded"
                    and pointer is None
                )
            else:
                generation = connection.execute("""
                    SELECT g.status, g.chunk_count
                    FROM published_generations p
                    JOIN article_generations g
                      ON g.configuration_id = p.configuration_id
                     AND g.article_path = p.article_path
                     AND g.generation_id = p.generation_id
                    WHERE p.configuration_id = ?
                      AND p.article_path = ?
                """, (configuration_id, article_path)).fetchone()

                eligible = (
                    article[0] == "completed"
                    and pointer is not None
                    and generation is not None
                    and generation[0] == "validated"
                    and generation[1] > 0
                )

            if not eligible:
                raise RuntimeError(
                    "Article not eligible for checkpoint advancement"
                )

            connection.execute("""
                INSERT INTO enumeration_checkpoints (
                    checkpoint_name,
                    last_article_title,
                    last_article_path,
                    articles_scanned,
                    configuration_id
                )
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(checkpoint_name) DO UPDATE SET
                    last_article_title = excluded.last_article_title,
                    last_article_path = excluded.last_article_path,
                    articles_scanned = excluded.articles_scanned,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                checkpoint_name,
                title,
                article_path,
                articles_scanned,
                configuration_id,
            ))

            connection.execute("COMMIT")

        except BaseException:
            if connection.in_transaction:
                connection.execute("ROLLBACK")
            raise
