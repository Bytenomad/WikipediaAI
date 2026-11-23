#!/usr/bin/env python3
"""
Script to create required Qdrant collections for Wikipedia AI.
"""

from qdrant_client import QdrantClient, models
from wikipedia_ai.ingestion.target import ACTIVE_COLLECTION, TEST_COLLECTION

def create_collections():
    """Create the required Qdrant collections."""
    
    client = QdrantClient(url="http://127.0.0.1:6333")
    
    # Create active collection
    try:
        client.create_collection(
            collection_name=ACTIVE_COLLECTION,
            vectors_config=models.VectorParams(
                size=768,
                distance=models.Distance.COSINE
            )
        )
        print(f"Created collection: {ACTIVE_COLLECTION}")
    except Exception as e:
        print(f"Error creating {ACTIVE_COLLECTION}: {e}")
    
    # Create test collection
    try:
        client.create_collection(
            collection_name=TEST_COLLECTION,
            vectors_config=models.VectorParams(
                size=768,
                distance=models.Distance.COSINE
            )
        )
        print(f"Created collection: {TEST_COLLECTION}")
    except Exception as e:
        print(f"Error creating {TEST_COLLECTION}: {e}")

if __name__ == "__main__":
    create_collections()