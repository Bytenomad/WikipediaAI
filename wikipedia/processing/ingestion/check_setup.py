#!/usr/bin/env python3
"""Final setup check for Wikipedia AI in remote Docker environment."""

import os
import sys

print("WIKIPEDIA AI SETUP CHECK")
print("=" * 40)

# Check that key components can be imported
try:
    # Test imports
    import test_chunking
    from batch_embeddings import EMBEDDING_MODEL, VECTOR_DIMENSIONS
    from qdrant_batch import ACTIVE_COLLECTION, client
    from ingestion_config import configuration_id
    
    print("✓ All core modules imported successfully")
    
    # Test configuration
    config_id = configuration_id()
    print(f"✓ Configuration fingerprint: {config_id[:32]}...")
    
    # Show relevant settings
    print(f"✓ Embedding model: {EMBEDDING_MODEL}")
    print(f"✓ Vector dimensions: {VECTOR_DIMENSIONS}")
    print(f"✓ Active collection: {ACTIVE_COLLECTION}")
    
    # Test Qdrant connection with remote address
    try:
        health = client.health_check()
        print("✓ Qdrant connection successful")
        print(f"  - Host: 192.168.2.96")
        print(f"  - Port: 6333")
        print(f"  - Status: {health}")
    except Exception as e:
        print(f"⚠ Qdrant health check failed: {e}")
        print("This might be expected if Qdrant is not yet running or not accessible.")
        
    print("\n" + "=" * 40)
    print("SETUP COMPLETE")
    print("Ready to process Wikipedia articles with:")
    print("python wikipedia/processing/ingestion/ingest_article.py \"Article Title\"")
    
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Setup error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nTo start processing Wikipedia articles:")
print("1. Make sure your ZIM file path is set in test_chunking.py")
print("2. Execute: python wikipedia/processing/ingestion/ingest_article.py \"Article Title\"")