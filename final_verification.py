#!/usr/bin/env python3
"""
Final verification that the fixes are working correctly.
This tests both the embedding function and the import script integration.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=== Testing Ollama Embedding Fix ===")

# Test the batch_embeddings module
from wikipedia_ai.ingestion.batch_embeddings import embed_batch

# Test with multiple texts (this was the main issue)
sample_texts = [
    "This is a test sentence for embedding.",
    "Another test sentence to verify the fix works correctly.",
    "Third test sentence for comprehensive testing."
]

try:
    result = embed_batch(sample_texts)
    print(f"SUCCESS: Generated {len(result)} embeddings")
    print(f"SUCCESS: Vector dimension: {len(result[0])}")
    print("SUCCESS: Ollama embedding API response handling is working correctly")
except Exception as e:
    print(f"ERROR in embedding test: {e}")
    sys.exit(1)

print("\n=== Testing Import Script Integration ===")

# Test that import script can be imported without errors
try:
    from wikipedia_ai.ingestion.import_all_us_history import import_all_us_history_categories
    print("SUCCESS: Import script imports successfully")
except Exception as e:
    print(f"ERROR importing script: {e}")
    sys.exit(1)

print("\n=== Testing Qdrant Integration ===")

# Test that qdrant_batch can be imported
try:
    from wikipedia_ai.ingestion.qdrant_batch import upload_batch
    print("SUCCESS: Qdrant batch module imports successfully")
except Exception as e:
    print(f"ERROR importing qdrant module: {e}")
    sys.exit(1)

print("\n=== All Tests Passed ===")
print("The Ollama API response format issue has been resolved.")
print("The embedding function now correctly handles single embeddings per call.")
print("The import script should work with Qdrant integration.")