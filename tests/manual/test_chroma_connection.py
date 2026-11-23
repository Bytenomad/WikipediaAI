#!/usr/bin/env python3
"""
Test script to verify Chroma database connection and data access.
"""

import _bootstrap

import sys
import os
sys.path.insert(0, 'src')

# Add the open-webui directory to path for database access
sys.path.append('open-webui')

try:
    from chromadb import Client
    from chromadb.config import Settings
    
    print("Testing Chroma database connection...")
    
    # Try to connect to the database
    client = Client()
    print("SUCCESS: Chroma client initialized successfully")
    
    # List collections
    collections = client.list_collections()
    print(f"Collections found: {len(collections)}")
    
    if len(collections) > 0:
        for collection in collections:
            print(f"Collection: {collection.name} with {collection.count()} items")
    else:
        print("No collections found - the database might be empty or not yet populated")
        
    print("\nDatabase connection test completed successfully!")
    
except Exception as e:
    print(f"ERROR connecting to Chroma: {e}")
    import traceback
    traceback.print_exc()