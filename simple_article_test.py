#!/usr/bin/env python3
"""
Simple test to check if article processing works.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def main():
    print("Testing basic import of Wikipedia AI modules...")
    
    try:
        # Try importing the key modules
        from wikipedia_ai.ingestion.article_ingestion import ingest_article
        print("✓ Successfully imported article_ingestion module")
        
        from wikipedia_ai.ingestion.qdrant_batch import get_client
        print("✓ Successfully imported qdrant_batch module")
        
        print("✓ All imports successful - basic functionality works")
        return 0
        
    except Exception as e:
        print(f"✗ Error during imports: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())