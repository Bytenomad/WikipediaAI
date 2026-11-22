"""Approved Qdrant destinations for Wikipedia ingestion."""

TEST_COLLECTION = "wikipedia_ingestion_test"
STAGING_COLLECTION = "wikipedia_staging_v1"

ALLOWED_INGESTION_COLLECTIONS = frozenset({
    TEST_COLLECTION,
    STAGING_COLLECTION,
})

# Keep the existing test destination active during migration.
ACTIVE_COLLECTION = STAGING_COLLECTION


def validate_ingestion_collection(collection):
    """Reject unapproved ingestion destinations."""
    if (
        not isinstance(collection, str)
        or collection not in ALLOWED_INGESTION_COLLECTIONS
    ):
        raise ValueError(
            f"Collection is not an approved ingestion destination: "
            f"{collection!r}"
        )

    return collection
