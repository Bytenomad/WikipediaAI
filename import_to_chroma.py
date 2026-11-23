
#!/usr/bin/env python3
"""Import script to populate Open WebUI's Chroma database with Qdrant data."""

import chromadb
import json
from pathlib import Path

def import_qdrant_export_to_chroma():
    """Import exported Qdrant data into Chroma."""
    
    # Connect to Chroma (Open WebUI's default location)
    client = chromadb.PersistentClient(path="./open-webui/vector_db")
    
    # Load the exported data
    with open("qdrant_export_for_openwebui.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Create or get collection
    collection_name = "wikipedia_articles"
    try:
        collection = client.get_collection(collection_name)
        print(f"Using existing collection: {collection_name}")
    except:
        collection = client.create_collection(collection_name)
        print(f"Created new collection: {collection_name}")
        
    # Import data
    for entry in data:
        # Chroma requires a unique ID, content, and metadata
        document_id = entry["id"]
        content = entry["content"]
        metadata = entry["metadata"]
        metadata["title"] = entry["title"]
        metadata["source"] = entry["source"]
        
        collection.add(
            ids=[document_id],
            documents=[content],
            metadatas=[metadata]
        )
        
    print(f"Successfully imported {len(data)} entries to Chroma")

if __name__ == "__main__":
    import_qdrant_export_to_chroma()
