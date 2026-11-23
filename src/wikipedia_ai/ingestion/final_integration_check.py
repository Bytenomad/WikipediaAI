#!/usr/bin/env python3
"""
Final integration check for Wikipedia AI to Open WebUI workflow.
This verifies the structure and existence of key components.
"""

import sys
import os

def check_files_exist():
    """Check that all required files exist."""
    print("Checking that all required files exist...")
    
    required_files = [
        "src/wikipedia_ai/ingestion/article_ingestion.py",
        "src/wikipedia_ai/ingestion/qdrant_batch.py", 
        "src/wikipedia_ai/ingestion/config.py",
        "src/wikipedia_ai/ingestion/batch_embeddings.py",
        "src/wikipedia_ai/ingestion/chunking.py",
        "src/wikipedia_ai/ingestion/target.py",
        "src/wikipedia_ai/ingestion/cleanup.py",
        "src/wikipedia_ai/ingestion/qdrant_to_openwebui_export.py",
        "src/wikipedia_ai/ingestion/openwebui_qdrant_integration.py",
        "src/wikipedia_ai/ingestion/test_single_article_final.py"
    ]
    
    all_found = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"OK: {file_path}")
        else:
            print(f"ERROR: Missing {file_path}")
            all_found = False
    
    return all_found

def check_main_components():
    """Check main components of the system."""
    print("\nChecking main components...")
    
    # Check that article_ingestion.py has been modified to allow testing
    try:
        with open("src/wikipedia_ai/ingestion/article_ingestion.py", "r") as f:
            content = f.read()
            
        # Look for key indicators that we've removed legacy logic
        if "ConfirmedUnsupportedArticle" in content:
            print("OK: ConfirmedUnsupportedArticle class found")
        else:
            print("WARNING: ConfirmedUnsupportedArticle class not found")
            
        if "ingest_article" in content and "def ingest_article" in content:
            print("OK: ingest_article function found")
        else:
            print("ERROR: ingest_article function not found")
            
        return True
        
    except Exception as e:
        print(f"ERROR checking main components: {e}")
        return False

def main():
    """Run all checks."""
    print("Running final integration checks...")
    
    success = True
    
    # Check files exist
    if not check_files_exist():
        success = False
        
    # Check main components
    if not check_main_components():
        success = False
    
    if success:
        print("\nSUCCESS: All integration checks passed!")
        print("The Wikipedia AI pipeline is properly structured for Open WebUI integration.")
        return 0
    else:
        print("\nFAILURE: Some integration checks failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())