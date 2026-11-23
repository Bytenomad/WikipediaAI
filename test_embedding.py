#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wikipedia_ai.ingestion.batch_embeddings import embed_batch

# Test with multiple texts
sample_texts = [
    "This is the first test sentence for embedding.",
    "This is the second test sentence for embedding.",
    "This is the third test sentence for embedding."
]

try:
    result = embed_batch(sample_texts)
    print(f"Generated {len(result)} embeddings")
    print(f"Vector dimension: {len(result[0]) if result else 0}")
    print("SUCCESS: Batch embedding generation works")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()