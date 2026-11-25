"""
Simple unit tests for service implementations that don't require complex mocking.
"""

import unittest
import sys
import os

# Add src to path so we can import properly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wikipedia_ai.ingestion.services.embedding_service import OllamaEmbeddingService
from wikipedia_ai.ingestion.services.qdrant_impl import QdrantServiceImpl


class TestEmbeddingServiceSimple(unittest.TestCase):
    """Simple test cases for embedding service - just checking instantiation works."""

    def test_embedding_service_instantiation(self):
        """Test that OllamaEmbeddingService can be instantiated."""
        service = OllamaEmbeddingService(
            model_name="test-model",
            base_url="http://localhost:11434"
        )
        
        self.assertIsInstance(service, OllamaEmbeddingService)
        self.assertEqual(service.model_name, "test-model")
        self.assertEqual(service.base_url, "http://localhost:11434")

    def test_embedding_service_method_exists(self):
        """Test that required methods exist."""
        service = OllamaEmbeddingService()
        
        # Check if the method exists and is callable
        self.assertTrue(hasattr(service, 'generate_embeddings'))
        self.assertTrue(callable(getattr(service, 'generate_embeddings')))


class TestQdrantServiceSimple(unittest.TestCase):
    """Simple test cases for Qdrant service - just checking instantiation works."""

    def test_qdrant_service_instantiation(self):
        """Test that QdrantServiceImpl can be instantiated."""
        service = QdrantServiceImpl()
        
        self.assertIsInstance(service, QdrantServiceImpl)

    def test_qdrant_service_method_exists(self):
        """Test that required methods exist."""
        service = QdrantServiceImpl()
        
        # Check if methods exist and are callable
        self.assertTrue(hasattr(service, 'initialize_collection'))
        self.assertTrue(hasattr(service, 'upload_batch'))
        self.assertTrue(hasattr(service, 'search'))
        
        self.assertTrue(callable(getattr(service, 'initialize_collection')))
        self.assertTrue(callable(getattr(service, 'upload_batch')))
        self.assertTrue(callable(getattr(service, 'search')))


if __name__ == '__main__':
    unittest.main()