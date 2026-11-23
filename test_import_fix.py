#!/usr/bin/env python3
"""
Simple test to verify the import_us_history.py fix works correctly.
"""

import sys
import os

# Add the parent directory (src) to Python path so modules can be imported properly
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

def test_import_fix():
    """Test that our import_us_history.py fix works."""
    try:
        # Test importing the module
        from src.wikipedia_ai.ingestion.import_us_history import get_articles_from_category
        
        print("SUCCESS: Successfully imported get_articles_from_category function")
        
        # Check if we can access the category_utils module
        from src.wikipedia_ai.ingestion.category_utils import get_articles_from_category as utils_get_articles
        
        print("SUCCESS: Successfully imported category_utils.get_articles_from_category function")
        
        print("All imports successful - fix appears to be working correctly!")
        return True
        
    except Exception as e:
        print(f"ERROR during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_import_fix()
    sys.exit(0 if success else 1)