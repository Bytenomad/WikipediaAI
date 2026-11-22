"""
Collection targeting for Wikipedia AI.
"""

# These collections should not be hard-coded but defined in config
ACTIVE_COLLECTION = "wikipedia_articles"
TEST_COLLECTION = "wikipedia_test_articles"

def validate_ingestion_collection(collection_name):
    """Verify collection is a valid target."""
    if collection_name not in (ACTIVE_COLLECTION, TEST_COLLECTION):
        raise ValueError(
            f"Invalid collection: {collection_name}. "
            f"Must be one of: {ACTIVE_COLLECTION}, {TEST_COLLECTION}"
        )