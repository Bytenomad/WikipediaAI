"""Test script to verify the ingestion pipeline setup."""

import sys
import os

# Add the project root to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported."""
    
    try:
        # Test basic functionality
        import test_chunking
        print("✓ test_chunking imported successfully")
        
        from batch_embeddings import embed_batch, EMBEDDING_MODEL, VECTOR_DIMENSIONS
        print(f"✓ batch_embeddings imported successfully (model: {EMBEDDING_MODEL})")
        
        from qdrant_batch import upload_batch, ACTIVE_COLLECTION
        print(f"✓ qdrant_batch imported successfully (collection: {ACTIVE_COLLECTION})")
        
        from article_generations import register_generation, validate_generation, fail_generation, publish_generation
        print("✓ article_generations imported successfully")
        
        from ingestion_progress import connect, register_article, start_article, complete_article, fail_article
        print("✓ ingestion_progress imported successfully")
        
        from ingestion_config import configuration_id, configuration_details
        print("✓ ingestion_config imported successfully")
        
        config_id = configuration_id()
        print(f"✓ Configuration ID generated: {config_id}")
        
        print("\nAll modules imported successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False

def verify_files_exist():
    """Verify that all necessary files exist."""
    
    required_files = [
        "test_chunking.py",
        "batch_embeddings.py", 
        "qdrant_batch.py",
        "qdrant_cleanup.py",
        "enumerate_articles.py"
    ]
    
    missing_files = []
    for filename in required_files:
        filepath = os.path.join("wikipedia", "processing", "ingestion", filename)
        if not os.path.exists(filepath):
            missing_files.append(filename)
    
    if missing_files:
        print(f"⚠ Missing files: {missing_files}")
        return False
    else:
        print("✓ All required files present")
        return True

if __name__ == "__main__":
    print("Testing Wikipedia AI ingestion pipeline setup...\n")
    
    success = True
    success &= verify_files_exist()
    success &= test_imports()
    
    if success:
        print("\n🎉 Setup verification complete - all components working!")
    else:
        print("\n❌ Setup verification failed - check error messages above.")
        sys.exit(1)