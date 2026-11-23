#!/usr/bin/env python3
"""Export data from Qdrant for Open WebUI compatibility."""

import sys
import os
from pathlib import Path

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
import json

def export_qdrant_to_openwebui_format():
    """Export Qdrant data in a format compatible with Open WebUI's Chroma database."""
    
    print("=== Exporting Qdrant Data for Open WebUI ===")
    
    try:
        # Connect to Qdrant
        client = QdrantClient(url="http://127.0.0.1:6333")
        
        # Check if collections exist
        collections = client.get_collections()
        print("Available collections:")
        for collection in collections.collections:
            print(f"  - {collection.name}")
            
        # Try to get data from the test collection (or active if it exists)
        collection_name = "wikipedia_test_articles"
        
        try:
            # Get all points from the collection
            points = client.scroll(
                collection_name=collection_name,
                limit=1000,  # Adjust as needed
                with_payload=True,
                with_vectors=True
            )
            
            print(f"Found {len(points[0])} points in collection '{collection_name}'")
            
            # Process the data to match Open WebUI format
            openwebui_data = []
            for point in points[0]:
                payload = point.payload
                
                # Convert Qdrant structure to a format that Open WebUI can use
                entry = {
                    "id": point.id,
                    "content": payload.get("text", ""),
                    "title": payload.get("title", ""),
                    "source": payload.get("source", ""),
                    "embedding_model": payload.get("embedding_model", ""),
                    "configuration_id": payload.get("configuration_id", ""),
                    "metadata": {
                        "section": payload.get("section", ""),
                        "article_path": payload.get("article_path", ""),
                        "chunk_index": payload.get("chunk_index", 0),
                        "kiwix_url": payload.get("kiwix_url", "")
                    }
                }
                
                openwebui_data.append(entry)
            
            # Save to a file for Open WebUI import
            output_file = "qdrant_export_for_openwebui.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(openwebui_data, f, indent=2, ensure_ascii=False)
                
            print(f"Exported {len(openwebui_data)} entries to {output_file}")
            print("This file can be used to populate Open WebUI's Chroma database")
            
            # Show sample of the exported data
            if openwebui_data:
                print("\nSample entry:")
                print(json.dumps(openwebui_data[0], indent=2, ensure_ascii=False))
                
        except Exception as e:
            print(f"Error reading from collection '{collection_name}': {e}")
            
            # Try to get data from active collection if test collection fails
            try:
                collection_name = "wikipedia_articles"
                points = client.scroll(
                    collection_name=collection_name,
                    limit=1000,
                    with_payload=True,
                    with_vectors=True
                )
                
                print(f"Found {len(points[0])} points in active collection '{collection_name}'")
                # Process and save as above...
                
            except Exception as e2:
                print(f"Error reading from active collection too: {e2}")
                print("No data found in either collection")
                
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")
        print("Make sure Qdrant is running on http://127.0.0.1:6333")

def create_chroma_import_script():
    """Create a script that can import the exported data into Chroma."""
    
    script_content = '''
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
'''
    
    with open("import_to_chroma.py", "w") as f:
        f.write(script_content)
    
    print("Created import_to_chroma.py script")
    print("Run this script after exporting Qdrant data to populate Open WebUI's Chroma")

if __name__ == "__main__":
    export_qdrant_to_openwebui_format()
    create_chroma_import_script()