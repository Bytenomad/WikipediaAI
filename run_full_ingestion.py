#!/usr/bin/env python3
"""
Full ingestion process for Wikipedia AI pipeline.
This script demonstrates the complete workflow from article processing to data export.
"""

import sys
import os
import json
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("=== Running Full Wikipedia AI Ingestion Process ===")
    
    try:
        # Import required modules
        from wikipedia_ai.ingestion.qdrant_batch import QdrantClient
        from wikipedia_ai.ingestion.article_ingestion import ingest_article
        from wikipedia_ai.ingestion.qdrant_to_openwebui_export import export_from_qdrant
        
        print("1. Checking Qdrant connection...")
        client = QdrantClient(url="http://127.0.0.1:6333")
        collections = [col.name for col in client.get_collections().collections]
        print(f"   [OK] Connected to Qdrant, found {len(collections)} collections")
        
        print("2. Processing sample article...")
        # Process a test article
        article_result = ingest_article("Testville")
        print(f"   [OK] Article processed: {article_result}")
        
        print("3. Exporting to Open WebUI format...")
        # Export data from Qdrant for Open WebUI
        exported_data = export_from_qdrant()
        print(f"   [OK] Exported {len(exported_data)} documents")
        
        # Save the exported data
        with open('qdrant_export.json', 'w') as f:
            json.dump(exported_data, f, indent=2)
        print("   [OK] Data saved to qdrant_export.json")
        
        print("\n=== PROCESS COMPLETED SUCCESSFULLY ===")
        print("Next steps:")
        print("1. Import qdrant_export.json into Open WebUI's Chroma database")
        print("2. Configure Open WebUI to use this database for chat functionality")
        
    except ImportError as e:
        print(f"[ERROR] Import error - check your Python path: {e}")
        return 1
    except Exception as e:
        print(f"[ERROR] Error during process: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())