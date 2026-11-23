#!/usr/bin/env python3
"""
Simple test to verify the Wikipedia AI pipeline components are working.
"""

import sys
import os

def test_basic_imports():
    """Test that we can import basic modules."""
    print("Testing basic imports...")
    
    try:
        # Test importing key modules
        sys.path.insert(0, 'src')
        
        # Try to import the main components
        from wikipedia_ai.ingestion import article_ingestion
        from wikipedia_ai.ingestion import qdrant_batch
        from wikipedia_ai.ingestion import config
        
        print("SUCCESS: All basic modules imported successfully")
        return True
        
    except Exception as e:
        print(f"ERROR importing modules: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_file_structure():
    """Test that key files exist."""
    print("Testing file structure...")
    
    required_files = [
        "src/wikipedia_ai/ingestion/article_ingestion.py",
        "src/wikipedia_ai/ingestion/qdrant_batch.py", 
        "src/wikipedia_ai/ingestion/config.py",
        "src/wikipedia_ai/ingestion/batch_embeddings.py",
        "src/wikipedia_ai/ingestion/chunking.py"
    ]
    
    all_found = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"FOUND: {file_path}")
        else:
            print(f"MISSING: {file_path}")
            all_found = False
    
    return all_found

def main():
    """Run all tests."""
    print("Running basic system verification tests...")
    
    success = True
    
    # Test imports
    if not test_basic_imports():
        success = False
        
    # Test structure  
    if not test_file_structure():
        success = False
    
    if success:
        print("\nSUCCESS: All basic tests passed!")
        print("The Wikipedia AI pipeline components are properly structured.")
        return 0
    else:
        print("\nFAILURE: Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())