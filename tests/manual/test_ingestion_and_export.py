#!/usr/bin/env python3
"""
Test script to process a real Wikipedia article and export it for Open WebUI.
This script will actually upload data to Qdrant and then export it.
"""

import _bootstrap

import sys
import os
import json

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("=== Testing Ingestion and Export Process ===")
    
    try:
        # Import required modules
        from wikipedia_ai.ingestion.qdrant_batch import QdrantClient
        from wikipedia_ai.ingestion.article_ingestion import ingest_article
        from wikipedia_ai.ingestion.qdrant_to_openwebui_export import export_from_qdrant
        
        print("1. Checking Qdrant connection...")
        client = QdrantClient(url="http://127.0.0.1:6333")
        collections = [col.name for col in client.get_collections().collections]
        print(f"   [OK] Connected to Qdrant, found {len(collections)} collections")
        
        # Test with a real article that should exist in the ZIM file
        print("2. Processing Wikipedia article...")
        test_title = "Medicine"
        article_result = ingest_article(test_title)
        print(f"   [OK] Article processed: {article_result}")
        
        print("3. Checking collections after ingestion...")
        collections = [col.name for col in client.get_collections().collections]
        print(f"   [OK] Found {len(collections)} collections after processing")
        for collection in collections:
            print(f"     - {collection}")
            
        print("4. Exporting to Open WebUI format...")
        # Export data from Qdrant for Open WebUI
        exported_data = export_from_qdrant()
        print(f"   [OK] Exported {len(exported_data)} documents")
        
        # Save the exported data
        with open('qdrant_export.json', 'w') as f:
            json.dump(exported_data, f, indent=2)
        print("   [OK] Data saved to qdrant_export.json")
        
        print("\n=== TEST COMPLETED SUCCESSFULLY ===")
        print("The qdrant_export.json file contains data ready for Open WebUI import.")
        
    except Exception as e:
        print(f"[ERROR] Error during process: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())