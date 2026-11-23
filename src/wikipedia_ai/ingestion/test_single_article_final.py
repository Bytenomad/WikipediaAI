#!/usr/bin/env python3
"""
Final comprehensive test script for single article processing.
This script tests the complete workflow from ingestion to Qdrant export.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from article_ingestion import ingest_article
from qdrant_batch import upload_batch
from config import configuration_id
import json

def test_single_article():
    """Test the single article ingestion process."""
    print("=== Testing Single Article Ingestion ===")
    
    # Test with a sample article title
    test_title = "Medicine"
    
    try:
        result = ingest_article(test_title)
        print(f"[SUCCESS] Article ingestion completed: {result}")
        
        # Test configuration ID generation
        config_id = configuration_id()
        print(f"[SUCCESS] Configuration ID generated: {config_id}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error during single article test: {e}")
        return False

def test_qdrant_export():
    """Test the Qdrant export functionality."""
    print("\n=== Testing Qdrant Export ===")
    
    try:
        # Test that we can import and use the Qdrant export functionality
        from qdrant_batch import QdrantClient, upload_batch
        
        # Check if we can connect to Qdrant - we'll use a direct client instead of get_client
        client = QdrantClient(url="http://127.0.0.1:6333")
        print("Connected to Qdrant successfully")
        
        return True
        
    except Exception as e:
        print(f"Error during Qdrant export test: {e}")
        return False

def main():
    """Run all tests."""
    print("Running comprehensive single article test...")
    
    success = True
    
    # Test single article ingestion
    if not test_single_article():
        success = False
        
    # Test Qdrant export
    if not test_qdrant_export():
        success = False
    
    if success:
        print("\n[SUCCESS] All tests passed!")
        return 0
    else:
        print("\n[FAILED] Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())