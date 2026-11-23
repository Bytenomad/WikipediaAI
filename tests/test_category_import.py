#!/usr/bin/env python3
"""
Test script for category-based Wikipedia article import functionality.
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the src directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from src.wikipedia_ai.ingestion.import_category_batch import (
    get_articles_from_category,
    import_category_batch
)

class TestCategoryImport(unittest.TestCase):

    def category_archive(self):
        archive = MagicMock()
        item = MagicMock()
        item.mimetype = "text/html"
        item.content = b'<div id="mw-pages"><a href="Test_Article">Test Article</a></div>'
        archive.get_entry_by_title.return_value.get_item.return_value = item
        return archive

    def test_get_articles_from_category(self):
        """Test getting articles from a category."""
        archive = self.category_archive()

        result = get_articles_from_category(archive, "Test Category")

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "Test Article")
        archive.get_entry_by_title.assert_called_once_with("Category:Test Category")

    @patch('src.wikipedia_ai.ingestion.import_category_batch.Archive')
    @patch('src.wikipedia_ai.ingestion.import_category_batch.article_html')
    @patch('src.wikipedia_ai.ingestion.import_category_batch.chunks_from_html')
    @patch('src.wikipedia_ai.ingestion.import_category_batch.extract_images_from_article')
    @patch('src.wikipedia_ai.ingestion.import_category_batch.format_response_with_images')
    @patch('src.wikipedia_ai.ingestion.import_category_batch.upload_batch')
    def test_import_category_batch(self, mock_upload_batch, mock_format_response, 
                                 mock_extract_images, mock_make_chunks, mock_article_html, 
                                 mock_archive):
        """Test importing a category batch."""
        mock_archive.return_value = self.category_archive()

        # Mock article HTML content
        mock_article_html.return_value = (
            "<html><body><div class='mw-parser-output'><p>Test content</p>"
            "</div></body></html>"
        )
        
        # Mock chunks and images
        mock_make_chunks.return_value = ["chunk1", "chunk2"]
        mock_extract_images.return_value = [{"url": "test.jpg", "alt": "Test image"}]
        mock_format_response.return_value = "Formatted response with images"
        
        # Mock upload_batch to do nothing (we're testing the flow)
        mock_upload_batch.return_value = None
        
        import_category_batch("Test Category", batch_size=2)

        mock_article_html.assert_called_once_with(mock_archive.return_value, "Test Article")
        mock_upload_batch.assert_called_once()

if __name__ == "__main__":
    unittest.main()
