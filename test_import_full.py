#!/usr/bin/env python3
"""
Test script to verify the import_all_us_history.py works correctly with all categories.
"""

import sys
import os

# Add the parent directory (src) to Python path so modules can be imported properly
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import required modules for testing
from wikipedia_ai.ingestion.import_all_us_history import (
    import_all_us_history_categories,
    US_HISTORY_CATEGORIES
)
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_import_with_small_batch():
    """Test the import with a small batch size to verify functionality."""
    logger.info("Starting test of full import functionality...")
    
    try:
        # Run with a small batch size for testing
        import_all_us_history_categories(batch_size=2)
        logger.info("Test completed successfully!")
        return True
    except Exception as e:
        logger.error(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_import_with_small_batch()
    sys.exit(0 if success else 1)