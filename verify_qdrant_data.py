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
            
        # Try to get some data from the collections
        for collection in collections.collections:
            if "wikipedia" in collection.name.lower():
                print(f"\nChecking collection: {collection.name}")
                
                # Get a few points from this collection
                try:
                    points = client.scroll(
                        collection_name=collection.name,
                        limit=5,
                        with_payload=True,
                        with_vectors=False
                    )
                    
                    print(f"Found {len(points[0])} points in collection")
                    if points[0]:
                        print("Sample data:")
                        for point in points[0][:2]:  # Show first 2 points
                            payload = point.payload
                            print(f"  ID: {point.id}")
                            print(f"  Title: {payload.get('title', 'N/A')}")
                            print(f"  Text preview: {payload.get('text', 'N/A')[:100]}...")
                            print()
                    else:
                        print("No data found in this collection")
                            
                except Exception as e:
                    print(f"Error reading from collection {collection.name}: {e}")
        
        print("Verification complete!")
        
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()