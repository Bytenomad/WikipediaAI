#!/usr/bin/env python3

import sys
import os

# Add the parent directory (src) to Python path so modules can be imported properly
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from wikipedia_ai.ingestion.config import configuration_id
from wikipedia_ai.ingestion.qdrant_batch import upload_batch

# Test the function call with sample data
def test_upload():
    try:
        # Sample test data
        article_title = "Test Article"
        article_path = "Test Article"  # This should be a string, not dict
        chunks = [{"text": "Sample chunk text", "chunk_index": "0", "section": "Introduction"}]
        vectors = [[0.1, 0.2, 0.3]] * len(chunks)  # Simple test vectors
        
        print("Testing upload_batch call...")
        print(f"article_title: {article_title}")
        print(f"article_path: {article_path} (type: {type(article_path)})")
        print(f"chunks: {chunks}")
        print(f"vectors: {vectors}")
        print(f"configuration_id(): {configuration_id()}")
        print(f"configuration_id type: {type(configuration_id())}")
        
        # This should work
        result = upload_batch(
            article_title=article_title,
            article_path=article_path,
            chunks=chunks,
            vectors=vectors,
            configuration_id=configuration_id(),  # Call the function to get the ID
            collection="test_collection",
            generation_id=None
        )
        
        print("Upload successful!")
        return True
        
    except Exception as e:
        print(f"Error in upload_batch: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_upload()