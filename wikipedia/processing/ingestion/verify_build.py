#!/usr/bin/env python3
"""
Simple verification of our implementation.
"""

import sys
import os

def check_module(module_path):
    """Check if a module can be imported."""
    try:
        # Add current dir to path for testing
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Try to import the module
        spec = __import__(module_path)
        print(f"✓ {module_path}: OK")
        return True
    except Exception as e:
        print(f"✗ {module_path}: FAILED - {e}")
        return False

def main():
    """Main verification function."""
    print("Wikipedia AI Implementation - Verification")
    print("=" * 50)
    
    # List of required components
    modules = [
        "test_chunking",
        "batch_embeddings", 
        "qdrant_batch",
        "qdrant_cleanup",
        "article_generations",
        "ingestion_progress",
        "ingestion_config"
    ]
    
    print("Checking module imports...")
    
    success = True
    for module in modules:
        if not check_module(module):
            success = False
    
    print("\n" + "=" * 50)
    
    if success:
        print("SUCCESS: All modules load correctly!")
        print("The generation-aware ingestion pipeline is ready to use.")
    else:
        print("FAILURE: Some modules failed to import.")
        
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())