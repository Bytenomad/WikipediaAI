#!/usr/bin/env python3
"""
Test script to verify Open WebUI chat functionality with Wikipedia data.
This script tests that the integration between Qdrant (Wikipedia AI) and Chroma (Open WebUI) works properly.
"""

import _bootstrap

import sys
import os
import time

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__) + '/src')

from wikipedia_ai.ingestion.test_single_article_final import test_single_article
from wikipedia_ai.ingestion.test_integration_final import test_integration
from wikipedia_ai.ingestion.config import configuration_id

def test_chat_functionality():
    """Test that Open WebUI can access and use Wikipedia data for chat."""
    print("=== Testing Open WebUI Chat Functionality ===")
    
    try:
        # Test the single article ingestion process first
        print("\n1. Testing single article ingestion...")
        success = test_single_article()
        if not success:
            print("[FAILED] Single article ingestion test failed")
            return False
        
        print("[SUCCESS] Single article ingestion test passed")
        
        # Test the full integration
        print("\n2. Testing full integration...")
        integration_success = test_integration()
        if not integration_success:
            print("[FAILED] Integration test failed")
            return False
            
        print("[SUCCESS] Integration test passed")
        
        # Test configuration ID generation
        print("\n3. Testing configuration ID generation...")
        config_id = configuration_id()
        print(f"[SUCCESS] Configuration ID generated: {config_id}")
        
        print("\n=== All Chat Functionality Tests Passed ===")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error during chat functionality testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_batch_ingestion():
    """Test batched ingestion functionality."""
    print("\n=== Testing Batched Ingestion ===")
    
    try:
        # Import the batched ingestion module
        from wikipedia_ai.ingestion.batched_ingestion import batch_process_articles
        
        print("Testing batch processing with a small set of articles...")
        
        # Test with a few sample articles (you may need to adjust this list)
        test_articles = ["Medicine", "Testville", "Python"]
        
        # This will process the articles in batches
        result = batch_process_articles(test_articles, batch_size=2)
        
        print(f"[SUCCESS] Batch processing completed with result: {result}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error during batch ingestion testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Open WebUI Chat Functionality Test")
    print("=" * 50)
    
    # Test chat functionality
    chat_success = test_chat_functionality()
    
    # Test batched ingestion
    batch_success = test_batch_ingestion()
    
    if chat_success and batch_success:
        print("\n🎉 ALL TESTS PASSED - Open WebUI is properly configured with Wikipedia data!")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED")
        sys.exit(1)