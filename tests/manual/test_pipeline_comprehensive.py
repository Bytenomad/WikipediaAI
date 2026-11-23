#!/usr/bin/env python3
"""
Comprehensive test script for the Wikipedia AI pipeline.
This script tests the complete workflow from ingestion to Qdrant storage.
"""

import _bootstrap

import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from wikipedia_ai.ingestion.article_ingestion import ingest_article
from wikipedia_ai.ingestion.qdrant_batch import upload_batch
from wikipedia_ai.ingestion.config import configuration_id
from qdrant_client import QdrantClient, models

def test_ingestion_pipeline():
    """Test the complete ingestion pipeline."""
    print("=== Testing Wikipedia AI Pipeline ===")
    
    # Test with a few sample articles
    test_articles = [
        "Testville",  # Our test article
        "Artificial intelligence",  # A real Wikipedia article for testing
    ]
    
    print(f"Configuration ID: {configuration_id()}")
    
    for article_title in test_articles:
        print(f"\n--- Testing article: {article_title} ---")
        try:
            result = ingest_article(article_title)
            print(f"SUCCESS: {article_title} - Result: {result}")
            
            # Simulate what would happen with actual data
            print("Simulating full ingestion process:")
            print("- Reading from ZIM archive (simulated)")
            print("- Extracting content")
            print("- Creating chunks")
            print("- Generating embeddings")
            print("- Uploading to Qdrant")
            
        except Exception as e:
            print(f"ERROR with {article_title}: {e}")
            # Continue with other articles
            continue
    
    print("\n=== Pipeline test completed ===")

def test_qdrant_connection():
    """Test connection to Qdrant."""
    print("\n=== Testing Qdrant Connection ===")
    
    try:
        client = QdrantClient(url="http://127.0.0.1:6333")
        
        # Check collections
        collections = client.get_collections()
        print("Collections in Qdrant:")
        for collection in collections.collections:
            print(f"  - {collection.name}")
            
        print("Qdrant connection successful!")
        return True
        
    except Exception as e:
        print(f"Failed to connect to Qdrant: {e}")
        return False

def test_sample_upload():
    """Test a sample upload to Qdrant."""
    print("\n=== Testing Sample Qdrant Upload ===")
    
    try:
        # Create some sample data
        chunks = [
            {"text": "This is a sample chunk of text for testing.", "section": "Introduction", "chunk_index": 0},
            {"text": "Another sample chunk for testing purposes.", "section": "Main Content", "chunk_index": 1}
        ]
        
        # Sample vectors (768 dimensions each)
        vectors = [
            [0.1] * 768,  # Sample vector
            [0.2] * 768   # Sample vector
        ]
        
        # Upload to Qdrant
        result = upload_batch(
            article_title="Test Article",
            article_path="/test/article",
            chunks=chunks,
            vectors=vectors,
            collection="wikipedia_test_articles",
            configuration_id=configuration_id(),
            generation_id="test_generation_123"
        )
        
        print(f"Successfully uploaded {result} points to Qdrant")
        return True
        
    except Exception as e:
        print(f"Upload test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Starting comprehensive pipeline tests...")
    
    # Test Qdrant connection first
    if not test_qdrant_connection():
        print("Qdrant connection test failed. Cannot proceed with full pipeline test.")
        return
    
    # Test ingestion pipeline
    test_ingestion_pipeline()
    
    # Test sample upload
    test_sample_upload()
    
    print("\n=== All tests completed ===")

if __name__ == "__main__":
    main()