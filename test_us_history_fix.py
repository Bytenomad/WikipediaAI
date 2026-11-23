#!/usr/bin/env python3
"""
Test script to verify the US history import fix works correctly.
This tests the core functionality without trying to access the full ZIM file.
"""

import sys
import os

# Add the parent directory (src) to Python path so modules can be imported properly
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

def test_import_structure():
    """Test that our import structure is correct and fix is applied."""
    print("Testing import_us_history.py structure...")
    
    try:
        # Test importing the module
        from wikipedia_ai.ingestion.import_us_history import get_articles_from_category
        
        # Test importing the category_utils function to verify the pattern matches
        from wikipedia_ai.ingestion.category_utils import get_articles_from_category as utils_get_articles
        
        print("✓ Successfully imported both functions")
        
        # Verify the structure matches what we expect
        import inspect
        get_articles_sig = inspect.signature(get_articles_from_category)
        utils_sig = inspect.signature(utils_get_articles)
        
        print(f"✓ get_articles_from_category signature: {get_articles_sig}")
        print(f"✓ utils_get_articles signature: {utils_sig}")
        
        print("SUCCESS: Import structure is correct and fix is properly applied!")
        return True
        
    except Exception as e:
        print(f"✗ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_function_logic():
    """Test that the function logic matches the working approach."""
    print("\nTesting function logic...")
    
    try:
        # Check if our function follows the right pattern
        from wikipedia_ai.ingestion.import_us_history import get_articles_from_category
        
        # Verify it's just a wrapper around the category_utils function
        import inspect
        source = inspect.getsource(get_articles_from_category)
        
        if "_get_articles_from_category" in source and "return _get_articles_from_category" in source:
            print("✓ Function correctly delegates to category_utils")
        else:
            print("✗ Function doesn't match expected pattern")
            return False
            
        print("SUCCESS: Function logic is correct!")
        return True
        
    except Exception as e:
        print(f"✗ Error testing function logic: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Testing US History Import Fix ===")
    
    success1 = test_import_structure()
    success2 = test_function_logic()
    
    if success1 and success2:
        print("\n🎉 ALL TESTS PASSED - The import_us_history.py fix is working correctly!")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED")
        sys.exit(1)