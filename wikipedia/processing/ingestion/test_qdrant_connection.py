#!/usr/bin/env python3
"""Simple test to check if Qdrant can be connected to."""

import os
try:
    from qdrant_client import QdrantClient
    
    # Try to connect to Qdrant with environment variables or default settings
    QDRANT_HOST = os.environ.get("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.environ.get("QDRANT_PORT", 6333))
    
    print(f"Attempting to connect to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}")
    
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    
    # Test connection with a simple health check
    try:
        health = client.health_check()
        print("✓ Qdrant is reachable and responding")
        print(f"Health check response: {health}")
    except Exception as e:
        print(f"⚠ Qdrant is reachable but health check failed: {e}")
        
    # List collections if successful
    try:
        collections = client.get_collections()
        print("✓ Collections found:")
        for collection in collections.collections:
            print(f"  - {collection.name}")
    except Exception as e:
        print(f"⚠ Could not retrieve collections: {e}")
        
    print("\nQdrant connection test completed successfully!")
    
except ImportError:
    print("⚠ Qdrant client not installed. Install with: pip install qdrant-client")
except Exception as e:
    print(f"✗ Qdrant connection failed: {e}")
    print("This might be expected if Qdrant is not running or accessible.")