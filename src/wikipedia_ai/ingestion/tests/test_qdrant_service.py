"""
Unit tests for the Qdrant service abstractions.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src to path so we can import properly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wikipedia_ai.ingestion.services.qdrant_service import VectorRecord
from wikipedia_ai.ingestion.services.qdrant_impl import QdrantServiceImpl


class TestQdrantServiceImpl(unittest.TestCase):
    """Test cases for QdrantServiceImpl."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.service = QdrantServiceImpl()

    @patch('wikipedia_ai.ingestion.services.qdrant_impl.QdrantClient')
    def test_initialize_collection(self, mock_qdrant_client):
        """Test collection initialization."""
        # Setup mock
        mock_client = MagicMock()
        mock_qdrant_client.return_value = mock_client
        
        # Test
        self.service.initialize_collection("test_collection", 768, "Cosine")
        
        # Verify (no actual calls expected since we assume collection exists)
        mock_qdrant_client.assert_called_once()

    @patch('wikipedia_ai.ingestion.services.qdrant_impl.QdrantClient')
    def test_upload_batch(self, mock_qdrant_client):
        """Test batch upload functionality."""
        # Setup mock
        mock_client = MagicMock()
        mock_qdrant_client.return_value = mock_client
        
        # Create test records
        records = [
            VectorRecord(
                id="1",
                vector=[0.1, 0.2, 0.3],
                metadata={},
                payload={"title": "Test Article", "text": "Test text"}
            ),
            VectorRecord(
                id="2",
                vector=[0.4, 0.5, 0.6],
                metadata={},
                payload={"title": "Test Article 2", "text": "More test text"}
            )
        ]
        
        # Test
        self.service.upload_batch("test_collection", records)
        
        # Verify
        mock_client.upsert.assert_called_once()


if __name__ == '__main__':
    unittest.main()