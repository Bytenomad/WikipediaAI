"""Cleanup operations for stale Wikipedia article chunks in Qdrant."""

from qdrant_client import QdrantClient
from ingestion_target import validate_ingestion_collection

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


def remove_article_chunks(article_path, collection, configuration_id, generation_id=None):
    """Remove all chunks for a specific article."""
    
    validate_ingestion_collection(collection)
    
    # Build filter for this article and configuration
    filters = [
        {"key": "article_path", "match": {"value": article_path}},
        {"key": "configuration_id", "match": {"value": configuration_id}}
    ]
    
    if generation_id is not None:
        filters.append({"key": "generation_id", "match": {"value": generation_id}})
        
    try:
        # Delete all points matching the filter
        result = client.delete(
            collection_name=collection,
            filter={"must": filters},
            wait=True
        )
        
        # Return count of deleted points
        return len(result.deleted) if hasattr(result, 'deleted') else 0
        
    except Exception as e:
        raise RuntimeError(f"Failed to remove article chunks: {e}")


def remove_stale_chunks(article_path, new_chunk_count, collection, configuration_id, generation_id=None):
    """Remove chunks from previous generations that are no longer relevant."""
    
    validate_ingestion_collection(collection)
    
    # Build filter for article and configuration
    filters = [
        {"key": "article_path", "match": {"value": article_path}},
        {"key": "configuration_id", "match": {"value": configuration_id}}
    ]
    
    if generation_id is not None:
        filters.append({"key": "generation_id", "match": {"value": generation_id}})
        
    try:
        # Count the number of points to be removed
        points = client.scroll(
            collection_name=collection,
            scroll_filter={"must": filters},
            limit=10000  # Adjust based on expected volume
        )
        
        deleted_count = 0
        for point in points[0]:
            # If point's chunk_index is not from the new chunks, it's stale
            if point.payload.get("chunk_index", -1) >= new_chunk_count:
                client.delete(
                    collection_name=collection,
                    points=[point.id],
                    wait=True
                )
                deleted_count += 1
                
        return deleted_count
        
    except Exception as e:
        raise RuntimeError(f"Failed to remove stale chunks: {e}")


if __name__ == "__main__":
    print("Qdrant cleanup module initialized")