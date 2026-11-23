#!/usr/bin/env python3
"""
Test script for batched ingestion with image support.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_batched_ingestion_with_images():
    """Test the updated batched ingestion with image support."""
    try:
        from src.wikipedia_ai.ingestion.batched_ingestion import run_batched_ingestion
        
        print("Testing updated batched ingestion with image support...")
        
        # Run a small test with just a few articles
        success = run_batched_ingestion(
            article_list_file=None,  # Use default test articles
            batch_size=5,             # Small batch size for testing
            collection_name="wikipedia_test_articles"
        )
        
        if success:
            print("✓ Batched ingestion with image support completed successfully!")
            return True
        else:
            print("✗ Batched ingestion failed")
            return False
            
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_batched_ingestion_with_images()