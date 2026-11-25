"""
Unit tests for the import_all_us_history.py script integration.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wikipedia_ai.ingestion.import_all_us_history import import_all_us_history_categories


class TestImportScript(unittest.TestCase):
    """Test cases for the import script integration."""

    @patch('wikipedia_ai.ingestion.import_all_us_history.Archive')
    @patch('wikipedia_ai.ingestion.import_all_us_history.get_articles_from_category')
    @patch('wikipedia_ai.ingestion.import_all_us_history.article_html')
    @patch('wikipedia_ai.ingestion.import_all_us_history.chunks_from_html')
    @patch('wikipedia_ai.ingestion.import_all_us_history.extract_images_from_article')
    @patch('wikipedia_ai.ingestion.import_all_us_history.format_response_with_images')
    @patch('wikipedia_ai.ingestion.import_all_us_history.OllamaEmbeddingService')
    @patch('wikipedia_ai.ingestion.import_all_us_history.QdrantServiceImpl')
    def test_import_all_us_history_categories(
        self,
        mock_qdrant_service,
        mock_embedding_service,
        mock_format_response,
        mock_extract_images,
        mock_chunks_from_html,
        mock_article_html,
        mock_get_articles,
        mock_archive
    ):
        """Test the main import function with mocked services."""
        # Setup mocks
        mock_zim_archive = MagicMock()
        mock_archive.return_value = mock_zim_archive
        
        mock_get_articles.return_value = ["Article 1", "Article 2"]
        
        mock_article_html.return_value = "<html>Sample HTML content</html>"
        
        mock_chunks_from_html.return_value = [
            {"section": "Introduction", "chunk_index": "0", "text": "First chunk"},
            {"section": "Body", "chunk_index": "1", "text": "Second chunk"}
        ]
        
        mock_extract_images.return_value = ["image1.jpg", "image2.jpg"]
        
        mock_format_response.return_value = "Formatted response"
        
        mock_embedding_service_instance = MagicMock()
        mock_embedding_service_instance.generate_embeddings.return_value = [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6]
        ]
        mock_embedding_service.return_value = mock_embedding_service_instance
        
        mock_qdrant_service_instance = MagicMock()
        # Mock that matches what the actual script is importing
        from wikipedia_ai.ingestion.services.qdrant_impl import QdrantServiceImpl
        
        # Since we're patching at a different level, we need to be more careful about this mock
        with patch('wikipedia_ai.ingestion.import_all_us_history.QdrantServiceImpl') as mock_qdrant_service:
            mock_qdrant_service_instance = MagicMock()
            mock_qdrant_service.return_value = mock_qdrant_service_instance
            
            # Test
            import_all_us_history_categories(batch_size=2)
            
            # Verify
            mock_get_articles.assert_called()
            mock_article_html.assert_called()
            mock_chunks_from_html.assert_called()
            mock_extract_images.assert_called()
            mock_format_response.assert_called()
            mock_embedding_service_instance.generate_embeddings.assert_called()
            mock_qdrant_service_instance.upload_batch.assert_called()
        
        # Test
        import_all_us_history_categories(batch_size=2)
        
        # Verify
        mock_get_articles.assert_called()
        mock_article_html.assert_called()
        mock_chunks_from_html.assert_called()
        mock_extract_images.assert_called()
        mock_format_response.assert_called()
        mock_embedding_service_instance.generate_embeddings.assert_called()
        mock_qdrant_service_instance.upload_batch.assert_called()


if __name__ == '__main__':
    unittest.main()