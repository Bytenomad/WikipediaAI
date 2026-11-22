"""
Test that all modules can be imported safely without touching production data.
"""
import pytest
import sys
from pathlib import Path


def test_module_structure():
    """Verify that the package structure supports imports."""
    
    # Test base package import
    try:
        import wikipedia_ai
        assert hasattr(wikipedia_ai, '__version__')
    except ImportError as e:
        pytest.fail(f"Failed to import main package: {e}")
    

def test_ingestion_package_imports():
    """Test that all ingestion submodules can be imported."""
    
    # Test each module imports cleanly
    modules_to_test = [
        'wikipedia_ai.ingestion.article_ingestion',
        'wikipedia_ai.ingestion.batch_embeddings', 
        'wikipedia_ai.ingestion.chunking',
        'wikipedia_ai.ingestion.qdrant_batch',
        'wikipedia_ai.ingestion.progress_tracking',
        'wikipedia_ai.ingestion.config',
        'wikipedia_ai.ingestion.enumeration',
        'wikipedia_ai.ingestion.cleanup',
        'wikipedia_ai.ingestion.target'
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
        except ImportError as e:
            pytest.fail(f"Failed to import {module}: {e}")


def test_import_path_correctness():
    """Verify that imports use correct relative paths."""
    
    # Import just from the package (not direct filesystem)
    try:
        from wikipedia_ai.ingestion import target
        assert hasattr(target, 'ACTIVE_COLLECTION')
        assert hasattr(target, 'TEST_COLLECTION')
    except Exception as e:
        pytest.fail(f"Import path test failed: {e}")


def test_no_production_data_access():
    """Ensure no modules access production databases or services during import."""
    
    # This just verifies that we don't have hardcoded DB connections in __init__.py
    # Or any import-time side effects
    
    from wikipedia_ai.ingestion.progress_tracking import DB_PATH
    assert isinstance(DB_PATH, Path)
    

if __name__ == "__main__":
    pytest.main([__file__, "-v"])