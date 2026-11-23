#!/usr/bin/env python3
"""
Integration script to connect Qdrant with Open WebUI's Chroma-based chat interface.
This script demonstrates the complete workflow from ingestion to chatting via Open WebUI.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
import json

def setup_qdrant_integration():
    """
    Set up the integration between Qdrant and Open WebUI.
    This involves:
    1. Processing single articles through the ingestion pipeline
    2. Storing them in Qdrant 
    3. Exporting data from Qdrant to a format compatible with Open WebUI's Chroma
    """
    
    print("=== Setting up Qdrant-Open WebUI Integration ===")
    
    # First, let's verify Qdrant is running
    try:
        client = QdrantClient(url="http://127.0.0.1:6333")
        print("✓ Successfully connected to Qdrant")
        
        # Check collections
        collections = client.get_collections()
        print("Available Qdrant collections:")
        for collection in collections.collections:
            print(f"  - {collection.name}")
            
    except Exception as e:
        print(f"✗ Error connecting to Qdrant: {e}")
        print("Make sure Qdrant is running on http://127.0.0.1:6333")
        return False
    
    return True

def test_single_article_ingestion():
    """
    Test single article processing using the existing pipeline.
    This demonstrates how to process a single article without requiring full ZIM archive.
    """
    
    print("\n=== Testing Single Article Ingestion ===")
    
    try:
        # Import required modules
        from wikipedia_ai.ingestion.article_ingestion import ingest_article
        
        # Test with a simple article title
        test_title = "Testville"
        print(f"Processing article: {test_title}")
        
        # This will use the modified ingestion logic that allows testing
        result = ingest_article(test_title)
        print(f"Ingestion result: {result}")
        
        return True
        
    except Exception as e:
        print(f"Error during single article ingestion: {e}")
        return False

def export_from_qdrant():
    """
    Export data from Qdrant in a format compatible with Open WebUI.
    """
    
    print("\n=== Exporting from Qdrant ===")
    
    try:
        # Connect to Qdrant
        client = QdrantClient(url="http://127.0.0.1:6333")
        
        # Try to get data from the test collection (or active if it exists)
        collections = client.get_collections()
        collection_name = None
        
        # Look for a Wikipedia collection
        for collection in collections.collections:
            if "wikipedia" in collection.name.lower():
                collection_name = collection.name
                break
                
        if not collection_name:
            # If no wikipedia collection found, use the first one
            if collections.collections:
                collection_name = collections.collections[0].name
            else:
                print("No collections found in Qdrant")
                return False
        
        print(f"Using collection: {collection_name}")
        
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
            
        return True
            
    except Exception as e:
        print(f"Error exporting from Qdrant: {e}")
        return False

def create_chroma_import_script():
    """
    Create a script that can import the exported data into Chroma (Open WebUI's database).
    """
    
    script_content = '''#!/usr/bin/env python3
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

def create_comprehensive_test():
    """
    Create a comprehensive test that demonstrates the complete workflow.
    """
    
    print("\n=== Comprehensive Integration Test ===")
    
    # Step 1: Setup integration
    if not setup_qdrant_integration():
        return False
    
    # Step 2: Test single article ingestion
    if not test_single_article_ingestion():
        print("Single article ingestion test failed")
        return False
    
    # Step 3: Export from Qdrant
    if not export_from_qdrant():
        print("Export from Qdrant failed")
        return False
    
    # Step 4: Create import script
    create_chroma_import_script()
    
    print("\n=== Integration Test Completed Successfully ===")
    print("\nWorkflow Summary:")
    print("1. Process single articles using the Wikipedia AI pipeline")
    print("2. Store them in Qdrant vector database") 
    print("3. Export data from Qdrant to Open WebUI compatible format")
    print("4. Import data into Open WebUI's Chroma database")
    print("5. Chat with the imported articles via Open WebUI")
    
    return True

if __name__ == "__main__":
    success = create_comprehensive_test()
    if not success:
        sys.exit(1)