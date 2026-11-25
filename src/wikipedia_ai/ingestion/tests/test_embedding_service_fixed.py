"""
Unit tests for the embedding service abstractions - fixed version.
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

    def test_generate_embeddings_success(self):
        """Test successful embedding generation."""
        # This is a simpler approach - we'll mock the requests call directly
        with patch('wikipedia_ai.ingestion.services.embedding_service.requests.post') as mock_post:
            # Setup mock response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'embedding': [0.1, 0.2, 0.3]
            }
            mock_post.return_value = mock_response
            
            # Test
            texts = ["Hello world", "Test sentence"]
            result = self.service.generate_embeddings(texts)
            
            # Verify
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0], [0.1, 0.2, 0.3])
            self.assertEqual(result[1], [0.1, 0.2, 0.3])

    def test_generate_embeddings_single_text(self):
        """Test embedding generation with single text."""
        with patch('wikipedia_ai.ingestion.services.embedding_service.requests.post') as mock_post:
            # Setup mock response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'embedding': [0.1, 0.2, 0.3]
            }
            mock_post.return_value = mock_response
            
            # Test
            texts = ["Hello world"]
            result = self.service.generate_embeddings(texts)
            
            # Verify
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0], [0.1, 0.2, 0.3])

    def test_generate_embeddings_empty_input(self):
        """Test embedding generation with empty input."""
        # Test that empty input returns empty list without making any requests
        result = self.service.generate_embeddings([])
        
        # Verify
        self.assertEqual(result, [])

    def test_generate_embeddings_error_handling(self):
        """Test error handling for failed API calls."""
        with patch('wikipedia_ai.ingestion.services.embedding_service.requests.post') as mock_post:
            # Setup mock response with error
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.text = "Server Error"
            mock_post.return_value = mock_response
            
            # Test that it raises a RuntimeError for API errors
            texts = ["Test text"]
            with self.assertRaises(RuntimeError):
                self.service.generate_embeddings(texts)


if __name__ == '__main__':
    unittest.main()