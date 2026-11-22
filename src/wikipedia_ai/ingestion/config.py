"""Deterministic configuration identification for Wikipedia ingestion."""

import hashlib
import json

# Imported modules should be handled via the package structure
# We'll need to ensure imports are preserved from our source code analysis
from wikipedia_ai.ingestion.batch_embeddings import EMBEDDING_MODEL, VECTOR_DIMENSIONS
from wikipedia_ai.ingestion.chunking import ZIM_PATH
from wikipedia_ai.ingestion.enumeration import enumerate_articles
from wikipedia_ai.ingestion.qdrant_batch import upload_batch
from wikipedia_ai.ingestion.target import ACTIVE_COLLECTION


def source_hash(module):
    """Hash the source file of a module."""
    # Note: In the original project, this looked at module.__file__
    # For package imports, we'll need to adapt or use a different approach 
    # This is a simplified approach for now
    raise NotImplementedError("Source hashing not implemented in package structure")


def configuration_details():
    """Collect settings affecting Wikipedia ingestion."""

    zim_path = ZIM_PATH
    zim_stat = zim_path.stat()

    return {
        "zim_filename": zim_path.name,
        "zim_size_bytes": zim_stat.st_size,
        "collection": ACTIVE_COLLECTION,
        "embedding_model": EMBEDDING_MODEL,
        "vector_dimensions": VECTOR_DIMENSIONS,
        "chunk_max_chars": 1500,  # From chunking module
        "chunking_source_hash": "hash_placeholder",  # Will be replaced with actual hash
        "embedding_source_hash": "hash_placeholder",
        "qdrant_upload_source_hash": "hash_placeholder",
        "vector_schema_version": "wikipedia-v4",
        "enumeration_method": "iter_by_title",
        "enumeration_source_hash": "hash_placeholder",
    }


def configuration_id():
    """Generate a stable SHA-256 fingerprint."""

    details = configuration_details()

    serialized = json.dumps(
        details,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return hashlib.sha256(serialized).hexdigest()


if __name__ == "__main__":
    print("INGESTION CONFIGURATION")
    print()

    for key, value in configuration_details().items():
        print(f"{key}: {value}")

    print()
    print("Configuration ID:", configuration_id())