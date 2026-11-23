#!/usr/bin/env python3
"""
Export script to transfer data from Qdrant to Open WebUI's Chroma-compatible format.
This script demonstrates how to extract data from Qdrant and convert it for use with Open WebUI.
"""

import sys
import os
from typing import List, Dict, Any
import json

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from qdrant_batch import QdrantClient
from config import configuration_id

def export_from_qdrant(collection_name: str = "wikipedia_test_articles") -> List[Dict[str, Any]]:
    """
    Export data from Qdrant collection for Open WebUI compatibility.
    
    Args:
        collection_name (str): Name of the Qdrant collection to export
        
    Returns:
        List[Dict[str, Any]]: List of documents in Open WebUI format
    """
    print(f"Exporting data from Qdrant collection: {collection_name}")
    
    try:
        client = QdrantClient(url="http://127.0.0.1:6333")
        
        # Check if collection exists first
        collections = [col.name for col in client.get_collections().collections]
        if collection_name not in collections:
            print(f"Collection '{collection_name}' does not exist. Available collections: {collections}")
            return []
        
        # Get all points from the collection
        points = client.scroll(
            collection_name=collection_name,
            limit=None,  # Get all points
            with_payload=True,
            with_vectors=False
        )
        
        documents = []
        for point in points[0]:  # Points are returned as a tuple (points, next_offset)
            payload = point.payload or {}
            
            # Convert Qdrant point to Open WebUI format
            document = {
                "id": point.id,
                "content": payload.get("text", ""),
                "metadata": {
                    "title": payload.get("title", ""),
                    "source": payload.get("source", ""),
                    "collection": collection_name,
                }
            }
            
            documents.append(document)
        
        print(f"Exported {len(documents)} documents from Qdrant")
        return documents
        
    except Exception as e:
        print(f"Error exporting from Qdrant: {e}")
        return []

def save_export_to_file(documents: List[Dict[str, Any]], filename: str = "qdrant_export.json"):
    """
    Save exported documents to a JSON file.
    
    Args:
        documents (List[Dict[str, Any]]): Documents to save
        filename (str): Name of the output file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(documents, f, indent=2, ensure_ascii=False)
        
        print(f"[SUCCESS] Saved export to {filename}")
        
    except Exception as e:
        print(f"[ERROR] Error saving export file: {e}")

def main():
    """Main function to run the Qdrant export test."""
    print("=== Testing Qdrant to Open WebUI Export ===")
    
    # Export data from Qdrant
    documents = export_from_qdrant()
    
    if documents:
        # Save to file
        save_export_to_file(documents)
        
        # Show sample of exported data
        print("\nSample of exported data:")
        for i, doc in enumerate(documents[:3]):  # Show first 3 documents
            print(f"Document {i+1}:")
            print(f"  ID: {doc['id']}")
            print(f"  Title: {doc['metadata']['title']}")
            content_preview = doc['content'][:100] if len(doc['content']) > 100 else doc['content']
            print(f"  Content preview: {content_preview.encode('ascii', 'ignore').decode('ascii')}...")
            print()
        
        return 0
    else:
        print("No documents exported")
        return 1

if __name__ == "__main__":
    sys.exit(main())