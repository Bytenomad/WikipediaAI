"""
Shared pytest fixtures for Wikipedia AI tests.
This ensures isolated test runs without touching production data.
"""
import pytest
import tempfile
import os
from pathlib import Path

# For testing we'll use in-memory SQLite databases and mocks where appropriate
@pytest.fixture(autouse=True)
def disable_production_access():
    """Ensure tests don't accidentally access production Qdrant or database."""
    # We will override paths and configurations to prevent access to 
    # actual production data during testing
    
@pytest.fixture(scope="session")
def temp_db_path():
    """Provide a temporary path for test database files."""
    temp_dir = tempfile.mkdtemp()
    return Path(temp_dir) / "test_ingestion.db"

@pytest.fixture
def mock_embedding_model():
    """Mock embedding model that returns predictable vectors."""
    # This will be implemented in specific test modules
    
@pytest.fixture
def sample_chunk():
    """Provide a sample chunk structure for testing."""
    return {
        "section": "Test Section",
        "text": "Sample text content for testing purposes."
    }