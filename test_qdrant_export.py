#!/usr/bin/env python3
"""
Simple test to verify Qdrant connection and export functionality.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'wikipedia_ai', 'ingestion'))

print("Testing Qdrant connection and export functionality...")

try:
    # Test basic imports
    from qdrant_batch import QdrantClient
    print("[SUCCESS] Successfully imported QdrantClient")
    
    # Try to connect to Qdrant
    client = QdrantClient(url="http://127.0.0.1:6333")
    print("[SUCCESS] Successfully connected to Qdrant at http://127.0.0.1:6333")
    
    # List collections to see what's there
    try:
        collections = client.get_collections()
        print(f"[SUCCESS] Collections found: {collections}")
    except Exception as e:
        print(f"[ERROR] Error listing collections: {e}")
        
except Exception as e:
    print(f"[ERROR] Error in basic test: {e}")

# Test the export functionality if possible
try:
    from qdrant_to_openwebui_export import export_from_qdrant
    print("[SUCCESS] Successfully imported export function")
    
    # Try to run export (this will likely fail if no data exists)
    documents = export_from_qdrant()
    print(f"[SUCCESS] Export completed, found {len(documents)} documents")
    
except Exception as e:
    print(f"[ERROR] Error in export test: {e}")