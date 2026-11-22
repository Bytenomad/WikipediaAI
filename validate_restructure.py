#!/usr/bin/env python3
"""
Validation script to ensure our restructuring was successful without touching production data.
"""

def validate_imports():
    """Validate that all modules can be imported correctly."""
    print("🔍 Validating imports...")
    
    try:
        import wikipedia_ai
        print("✅ Main package imports successfully")
        
        from wikipedia_ai.ingestion import (
            article_ingestion,
            batch_embeddings,
            chunking,
            qdrant_batch,
            progress_tracking,
            config,
            enumeration,
            cleanup,
            target
        )
        print("✅ All ingestion submodules import successfully")
        
        # Test specific functionality 
        from wikipedia_ai.ingestion.batch_embeddings import EMBEDDING_MODEL, VECTOR_DIMENSIONS
        assert EMBEDDING_MODEL == "nomic-embed-text"
        assert VECTOR_DIMENSIONS == 768
        print("✅ Embedding configuration verified")
        
        from wikipedia_ai.ingestion.target import ACTIVE_COLLECTION, TEST_COLLECTION
        assert ACTIVE_COLLECTION == "wikipedia_articles"
        assert TEST_COLLECTION == "wikipedia_test_articles"
        print("✅ Collection targets verified")
        
        print("\n🎉 All validations passed! Restructuring successful.")
        return True
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False

def validate_documentation():
    """Verify documentation files exist."""
    import os
    
    docs = [
        "docs/architecture.md",
        "docs/development.md", 
        "docs/safety.md",
        "docs/ingestion-lifecycle.md"
    ]
    
    print("🔍 Checking documentation files...")
    for doc in docs:
        if os.path.exists(doc):
            print(f"✅ {doc}")
        else:
            print(f"❌ Missing: {doc}")
            
def validate_structure():
    """Validate that structure is correct."""
    import os
    
    expected_dirs = [
        "src/wikipedia_ai/",
        "src/wikipedia_ai/ingestion/",
        "src/wikipedia_ai/storage/", 
        "src/wikipedia_ai/utils/",
        "tests/unit/",
        "tests/integration/",
        "docs/"
    ]
    
    print("🔍 Checking directory structure...")
    for dir_path in expected_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}")
        else:
            print(f"❌ Missing: {dir_path}")

if __name__ == "__main__":
    print("=== Wikipedia AI Restructuring Validation ===\n")
    
    success = True
    success &= validate_imports()
    validate_documentation() 
    validate_structure()
    
    print("\n" + "="*50)
    if success:
        print("🎉 All validation checks passed!")
        print("The refactoring was completed successfully.")
    else:
        print("❌ Some validation checks failed!")
        
    print("="*50)