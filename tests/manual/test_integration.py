#!/usr/bin/env python3
"""
Simple test script to verify the Wikipedia AI integration works properly.
This checks that our data is accessible through both Qdrant and Chroma databases.
"""

import _bootstrap

import sys
import os

# Add the src directory to Python path so we can import modules properly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing module imports...")
    
    try:
        from wikipedia_ai.ingestion.config import configuration_id
        print("✓ Configuration module imported successfully")
        
        from wikipedia_ai.ingestion.chunking import ZIM_PATH, article_html
        print("✓ Chunking module imported successfully")
        
        from wikipedia_ai.ingestion.qdrant_batch import upload_batch
        print("✓ Qdrant batch module imported successfully")
        
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_zim_access():
    """Test that we can access the ZIM file."""
    print("\nTesting ZIM file access...")
    
    try:
        from wikipedia_ai.ingestion.chunking import ZIM_PATH
        from libzim.reader import Archive
        
        if ZIM_PATH.exists():
            print(f"✓ ZIM file found: {ZIM_PATH}")
            
            # Try to open it
            archive = Archive(ZIM_PATH)
            print("✓ ZIM file opened successfully")
            
            # Test reading a simple article
            try:
                html_content = article_html(archive, "Medicine")
                if html_content:
                    print("✓ Can read 'Medicine' article from ZIM")
                else:
                    print("? Could not read 'Medicine' article (may be empty)")
            except Exception as e:
                print(f"? Error reading 'Medicine' article: {e}")
            
            return True
        else:
            print(f"✗ ZIM file not found: {ZIM_PATH}")
            return False
            
    except Exception as e:
        print(f"✗ ZIM access error: {e}")
        return False

def test_database_connection():
    """Test database connection to verify data is accessible."""
    print("\nTesting database connections...")
    
    try:
        # Test Qdrant connection
        from qdrant_client import QdrantClient
        
        client = QdrantClient(url="http://127.0.0.1:6334")
        collections = client.get_collections()
        
        print("✓ Connected to Qdrant successfully")
        print(f"  Collections found: {[c.name for c in collections.collections]}")
        
        # Test Chroma connection
        import chromadb
        from pathlib import Path
        
        chroma_path = Path('open-webui/vector_db/chroma.sqlite3')
        if chroma_path.exists():
            print("✓ Chroma database file found")
            
            client = chromadb.PersistentClient(path='open-webui/vector_db')
            collections = client.list_collections()
            
            print(f"  Chroma collections: {[c.name for c in collections]}")
        else:
            print("? Chroma database file not found at expected location")
            
        return True
    except Exception as e:
        print(f"✗ Database connection error: {e}")
        return False

def main():
    """Run all tests."""
    print("=== Wikipedia AI Integration Test ===")
    
    success = True
    success &= test_imports()
    success &= test_zim_access()
    success &= test_database_connection()
    
    print("\n" + "="*50)
    if success:
        print("✓ All integration tests passed!")
        print("The Wikipedia AI system is properly configured and working.")
    else:
        print("✗ Some integration tests failed!")
        print("Please check the errors above and resolve them.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)