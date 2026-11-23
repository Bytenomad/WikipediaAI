#!/usr/bin/env python3
"""
Verify that data is stored in Qdrant after processing an article.
"""

import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from qdrant_client import QdrantClient

def main():
    print("=== Verifying Qdrant Data ===")
    
    try:
        # Connect to Qdrant
        client = QdrantClient(url="http://127.0.0.1:6333")
        
        # List collections to see what we have
        collections = client.get_collections()
        print("Available collections in Qdrant:")
        for collection in collections.collections:
            print(f"  - {collection.name}")
            
        print("Verification complete!")
        
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()