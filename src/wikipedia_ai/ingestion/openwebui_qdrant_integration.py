#!/usr/bin/env python3
"""
Integration script demonstrating how to connect Qdrant and Open WebUI.
This shows the workflow from ingestion through to chat interface compatibility.
"""

import sys
import os
from typing import List, Dict, Any

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from qdrant_batch import QdrantClient
from config import configuration_id

def demonstrate_integration():
    """
    Demonstrate the complete integration workflow.
    """
    print("=== Qdrant to Open WebUI Integration Demo ===")
    
    try:
        # 1. Connect to Qdrant
        print("\n1. Connecting to Qdrant...")
        client = QdrantClient(url="http://127.0.0.1:6333")
        print("SUCCESS: Connected to Qdrant successfully")
        
        # 2. Get configuration info
        print("\n2. Getting configuration...")
        config_id = configuration_id()
        print(f"SUCCESS: Configuration ID: {config_id}")
        
        # 3. List collections
        print("\n3. Listing Qdrant collections...")
        collections = client.get_collections()
        print("Collections in Qdrant:")
        for collection in collections.collections:
            print(f"  - {collection.name}")
        
        # 4. Test data export capability
        print("\n4. Testing data export capability...")
        from wikipedia_ai.ingestion.qdrant_to_openwebui_export import export_from_qdrant
        
        # Try to export from the main collection if it exists
        collections_list = [col.name for col in collections.collections]
        main_collection = "wikipedia_articles" if "wikipedia_articles" in collections_list else None
        
        if main_collection:
            documents = export_from_qdrant(main_collection)
            print(f"SUCCESS: Successfully exported {len(documents)} documents")
        else:
            print("WARNING: No 'wikipedia_articles' collection found - this is expected if no data ingested yet")
        
        print("\n=== Integration Demo Complete ===")
        print("This demonstrates how Qdrant data can be accessed and converted for Open WebUI.")
        print("Open WebUI's Chroma database would need to be populated with similar data.")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Error in integration demo: {e}")
        return False

def main():
    """Run the integration demonstration."""
    success = demonstrate_integration()
    
    if success:
        print("\nSUCCESS: Integration demonstration completed successfully!")
        return 0
    else:
        print("\nERROR: Integration demonstration failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())