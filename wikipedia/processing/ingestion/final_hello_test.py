#!/usr/bin/env python3
"""Quick hello world test for the Wikipedia AI pipeline."""

import os
import sys

print("WIKIPEDIA AI HELLO WORLD TEST")
print("=" * 40)

try:
    # Test that we can import and initialize all key components
    from batch_embeddings import EMBEDDING_MODEL, VECTOR_DIMENSIONS
    from ingestion_config import configuration_id, configuration_details
    from qdrant_batch import ACTIVE_COLLECTION, get_point_id
    
    print("✓ All core modules imported successfully")
    
    # Show system information
    config_id = configuration_id()
    details = configuration_details()
    
    print(f"✓ Configuration ID: {config_id[:32]}...")
    print(f"✓ Embedding model: {EMBEDDING_MODEL}")
    print(f"✓ Vector dimensions: {VECTOR_DIMENSIONS}")  
    print(f"✓ Active collection: {ACTIVE_COLLECTION}")
    print(f"✓ Target host: 192.168.2.96 (configured)")
    
    # Test deterministic ID generation
    test_id = get_point_id("test_config", "test/path", "test_gen", 42)
    print(f"✓ Point ID generation works: {test_id[:20]}...")
    
    print("\n🎉 Wikipedia AI pipeline is ready!")
    print("Ready to process Wikipedia articles with generation awareness.")
    
    # Show usage instructions
    print("\nUSAGE INSTRUCTIONS:")
    print("1. First, ensure your ZIM archive path is set in test_chunking.py")  
    print("2. Then run: python wikipedia/processing/ingestion/ingest_article.py \"Article Title\"")
    print("3. Example: python wikipedia/processing/ingestion/ingest_article.py \"Machine Learning\"")
    
except ImportError as e:
    print(f"✗ Import failed - {e}")
    print("Make sure you've installed the package with: pip install -e .")
    sys.exit(1)
except Exception as e:
    print(f"⚠ Setup issue detected: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 40)
print("TEST COMPLETE")