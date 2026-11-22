"""Qdrant batch upload with generation-aware point IDs."""

import uuid
import hashlib
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Filter, FieldCondition, MatchValue
from ingestion_target import validate_ingestion_collection
import os

# Test collection (for development)
TEST_COLLECTION = "wikipedia_ingestion_test"
STAGING_COLLECTION = "wikipedia_staging_v1"

ACTIVE_COLLECTION = STAGING_COLLECTION

# Configuration for Qdrant client - adjust based on your setup
# Default to remote host IP address for Docker environment
QDRANT_HOST = os.environ.get("QDRANT_HOST", "192.168.2.96") 
QDRANT_PORT = int(os.environ.get("QDRANT_PORT", 6333))

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def get_point_id(configuration_id, article_path, generation_id, chunk_index):
    """Generate deterministic point ID using UUID5."""
    
    # Create a unique identifier based on all relevant components
    unique_string = f"{configuration_id}:{article_path}:{generation_id}:{chunk_index}"
    
    # Generate UUID5 based on the unique string (using DNS namespace for consistency)
    point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, unique_string))
    
    return point_id


def upload_batch(
    title,
    article_path,
    indexed_chunks,
    vectors,
    collection,
    configuration_id,
    generation_id=None
):
    """Upload a batch of chunks and their embeddings to Qdrant."""
    
    # Validate the target collection
    validate_ingestion_collection(collection)
    
    if len(indexed_chunks) != len(vectors):
        raise ValueError("Number of chunks must match number of vectors")
        
    points = []
    
    for idx, (chunk, vector) in enumerate(zip(indexed_chunks, vectors)):
        point_id = get_point_id(
            configuration_id, 
            article_path, 
            generation_id, 
            chunk["chunk_index"]
        )
        
        points.append({
            "id": point_id,
            "vector": vector,
            "payload": {
                "title": title,
                "article_path": article_path,
                "chunk_index": chunk["chunk_index"],
                "section": chunk["section"],
                "text": chunk["text"],
                "configuration_id": configuration_id,
                "generation_id": generation_id,
                "created_at": "CURRENT_TIMESTAMP"
            }
        })
        
    # Upload in batch to Qdrant
    try:
        client.upsert(
            collection_name=collection,
            points=points,
            wait=True
        )
        
        return len(points)
        
    except Exception as e:
        raise RuntimeError(f"Failed to upload batch to Qdrant: {e}")


if __name__ == "__main__":
    print("Qdrant batch upload module initialized")