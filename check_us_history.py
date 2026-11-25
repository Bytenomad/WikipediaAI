#!/usr/bin/env python3
"""
Check if US history data exists in the Qdrant database.
"""

import json
from qdrant_client import QdrantClient

def check_collection_content():
    """Check what's in the existing Qdrant collections."""
    
    # Connect to Qdrant on port 6334 (which we confirmed is running)
    client = QdrantClient(url="http://127.0.0.1:6334")
    
    # Get collections
    collections = client.get_collections()
    print("Available collections in Qdrant:")
    for collection in collections.collections:
        print(f"  - {collection.name}")
        
        # Check if there are any points in the collection
        try:
            count = client.count(collection_name=collection.name)
            print(f"    Total points: {count.count}")
            
            # Get some sample points to analyze content
            if count.count > 0:
                points = client.scroll(
                    collection_name=collection.name,
                    limit=min(5, count.count),
                    with_payload=True
                )
                
                for point in points[0]:
                    payload = point.payload
                    title = payload.get('title', 'No title')
                    print(f"      Sample title: {title}")
                    
        except Exception as e:
            print(f"    Error getting sample data: {e}")

def check_exported_data():
    """Check the qdrant_export.json file for US history content."""
    try:
        with open('qdrant_export.json', 'r') as f:
            data = json.load(f)
            
        us_history_titles = []
        print("\nChecking exported data for US History related titles:")
        
        for item in data[:20]:  # Check first 20 entries
            title = item.get('metadata', {}).get('title', '')
            if any(keyword in title.lower() for keyword in ['american', 'united', 'history']):
                us_history_titles.append(title)
                
        if us_history_titles:
            print("Found US History related titles:")
            for title in us_history_titles[:10]:  # Show top 10
                print(f"  - {title}")
        else:
            print("No obvious US History related titles found in exported data")
            
    except Exception as e:
        print(f"Error reading/exported data: {e}")

if __name__ == "__main__":
    print("=== Checking Qdrant Database Content ===")
    check_collection_content()
    print("\n=== Checking Exported Data ===")  
    check_exported_data()