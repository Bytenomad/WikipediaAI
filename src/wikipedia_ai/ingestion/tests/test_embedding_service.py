"""
Unit tests for the embedding service abstractions.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add src to path so we can import properly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wikipedia_ai.ingestion.services.embedding_service import OllamaEmbeddingService


class TestOllamaEmbeddingService(unittest.TestCase):
    """Test cases for OllamaEmbeddingService."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.service = OllamaEmbeddingService(
            model_name="test-model",
            base_url="http://localhost:11434"
        )

    @patch('wikipedia_ai.ingestion.services.embedding_service.ollama.embeddings')
    def test_generate_embeddings_success(self, mock_embeddings):
        """Test successful embedding generation."""
        # Setup mock
        mock_embeddings.return_value = {
            'embeddings': [
                [0.1, 0.2, 0.3],
                [0.4, 0.5, 0.6]
            ]
        }
        
        # Test
        texts = ["Hello world", "Test sentence"]
        result = self.service.generate_embeddings(texts)
        
        # Verify
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], [0.1, 0.2, 0.3])
        self.assertEqual(result[1], [0.4, 0.5, 0.6])
        mock_embeddings.assert_called_once_with(
            model="test-model",
            prompt="Hello world"
        )

    @patch('wikipedia_ai.ingestion.services.embedding_service.ollama.embeddings')
    def test_generate_embeddings_single_text(self, mock_embeddings):
        """Test embedding generation with single text."""
        # Setup mock
        mock_embeddings.return_value = {
            'embeddings': [[0.1, 0.2, 0.3]]
        }
        
        # Test
        texts = ["Hello world"]
        result = self.service.generate_embeddings(texts)
        
        # Verify
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], [0.1, 0.2, 0.3])
        mock_embeddings.assert_called_once_with(
            model="test-model",
            prompt="Hello world"
        )

    @patch('wikipedia_ai.ingestion.services.embedding_service.ollama.embeddings')
    def test_generate_embeddings_empty_input(self, mock_embeddings):
        """Test embedding generation with empty input."""
        # Test
        result = self.service.generate_embeddings([])
        
        # Verify
        self.assertEqual(result, [])
        mock_embeddings.assert_not_called()


if __name__ == '__main__':
    unittest.main()