"""
Test that the new ingestion structure imports properly and has correct dependencies.
"""
import pytest


def test_package_imports():
    """Test that main modules can be imported without issues."""
    
    # Test basic import functionality
    try:
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
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import package components: {e}")


def test_basic_functionality():
    """Test that basic functionalities of moved modules work."""
    
    # Test that batch_embeddings can be imported
    from wikipedia_ai.ingestion.batch_embeddings import EMBEDDING_MODEL, VECTOR_DIMENSIONS
    assert EMBEDDING_MODEL == "nomic-embed-text"
    assert VECTOR_DIMENSIONS == 768
    
    # Test that configuration module can be imported  
    from wikipedia_ai.ingestion.config import configuration_id
    # This should not error but won't generate real fingerprints without proper setup


def test_progress_module_import():
    """Test that progress tracking module works."""
    from wikipedia_ai.ingestion.progress_tracking import validate_configuration_id
    assert callable(validate_configuration_id)
    

def test_chunking_import():
    """Test that chunking module imports correctly."""
    from wikipedia_ai.ingestion.chunking import (
        make_chunks, 
        eligible_records,
        article_html,
        ZIM_PATH
    )
    # These should all be importable without errors


if __name__ == "__main__":
    pytest.main([__file__, "-v"])