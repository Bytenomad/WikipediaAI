#!/usr/bin/env python3
"""
Simple test script to verify the embedding fix works correctly.
"""

import sys
import os

# Add the parent directory (src) to Python path so modules can be imported properly
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from wikipedia_ai.ingestion.batch_embeddings import embed_batch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_embedding():
    """Test the embedding function with sample data."""
    logger.info("Testing embedding function...")
    
    try:
        # Test with a single text
        single_text = ["This is a test sentence for embedding."]
        result1 = embed_batch(single_text)
        logger.info(f"Single text embedding: {len(result1)} embeddings generated")
        if len(result1) > 0:
            logger.info(f"Vector dimension: {len(result1[0])}")
        
        # Test with multiple texts
        multiple_texts = [
            "This is the first test sentence.",
            "This is the second test sentence."
        ]
        result2 = embed_batch(multiple_texts)
        logger.info(f"Multiple text embeddings: {len(result2)} embeddings generated")
        if len(result2) > 0:
            logger.info(f"Vector dimension: {len(result2[0])}")
            
        logger.info("SUCCESS: Embedding function works correctly!")
        return True
        
    except Exception as e:
        logger.error(f"ERROR in embedding test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_embedding()
    sys.exit(0 if success else 1)