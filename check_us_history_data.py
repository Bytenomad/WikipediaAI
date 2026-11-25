#!/usr/bin/env python3
"""
Simple test to check if US history data has been properly imported into Qdrant.
"""
import sys
sys.path.insert(0, 'src')

from qdrant_client import QdrantClient

def main():
    print("=== Checking US History Data in Qdrant ===")
    
    # Initialize client
    client = QdrantClient(url='http://127.0.0.1:6334')
    
    try:
        # List collections
        collections = client.get_collections()
        print("Collections in Qdrant:")
        for collection in collections.collections:
            print(f"  - {collection.name}")
            
        # Get info about our test collection
        collection_info = client.get_collection(collection_name='wikipedia_test_articles')
        print(f"\nCollection 'wikipedia_test_articles' status: {collection_info.status}")
        
        # Show first few documents 
        points = client.scroll(
            collection_name='wikipedia_test_articles',
            limit=3,
            with_payload=True,
            with_vectors=False
        )
        
        print("\nSample documents in collection:")
        for i, point in enumerate(points[0]):
            title = point.payload.get('title', 'N/A')
            print(f"  {i+1}. Title: {title}")
            
        print("\n=== Verification Complete ===")
        print("If we can see US history content like 'United States', 'American Civil War', etc.,")
        print("then the import was successful.")
        
    except Exception as e:
        print(f"Error checking collection: {e}")

if __name__ == "__main__":
    main()