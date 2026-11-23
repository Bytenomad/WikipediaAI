#!/usr/bin/env python3
"""
Example script demonstrating how to use the category-based import functionality.

This script shows different ways to import Wikipedia articles by category.
"""

import sys
import os

# Add src directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

def main():
    print("Wikipedia Category Import Example")
    print("=" * 40)
    
    print("\n1. Basic usage:")
    print("   python import_category_batch.py \"Medicine\" 5")
    print("   This imports articles from the 'Medicine' category in batches of 5")
    
    print("\n2. Different category:")
    print("   python import_category_batch.py \"Science\" 10")
    print("   This imports articles from the 'Science' category in batches of 10")
    
    print("\n3. Default batch size:")
    print("   python import_category_batch.py \"History\"")
    print("   This imports articles from the 'History' category with default batch size (10)")
    
    print("\n4. Environment variable override:")
    print("   export ZIM_PATH=/path/to/your/wikipedia.zim")
    print("   python import_category_batch.py \"Technology\" 3")
    print("   This uses a custom ZIM file path")
    
    print("\nNote: Make sure the Wikipedia ZIM file is in the correct location")
    print("      and that Docker volumes are properly configured for image storage.")

if __name__ == "__main__":
    main()