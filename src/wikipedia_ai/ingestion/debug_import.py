#!/usr/bin/env python3
"""
Debug script for import_all_us_history to see what's happening.
"""

import sys
import os
from pathlib import Path

# Add the parent directory (src) to Python path so modules can be imported properly
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import required modules
from libzim.reader import Archive
from wikipedia_ai.ingestion.category_utils import get_articles_from_category as _get_articles_from_category

# Import chunking functions
from wikipedia_ai.ingestion.chunking import (
    ZIM_PATH,
    article_html,
    chunks_from_html,
)
from wikipedia_ai.ingestion.qdrant_batch import upload_batch
from wikipedia_ai.ingestion.config import configuration_id
from wikipedia_ai.ingestion.target import ACTIVE_COLLECTION, TEST_COLLECTION
from wikipedia_ai.ingestion.batch_embeddings import embed_batch
import json

# Import image extraction functionality
from wikipedia_ai.ingestion.image_extraction import (
    extract_images_from_article
)
from wikipedia_ai.ingestion.response_formatter import format_response_with_images

# Import logging
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def debug_import():
    """Debug the import process with a small sample."""
    try:
        # Open the ZIM archive
        logger.info(f"Opening ZIM archive at {ZIM_PATH}")
        zim_archive = Archive(ZIM_PATH)
        
        # Test with just one category for debugging
        category_name = "United States"
        logger.info(f"Retrieving articles from category: {category_name}")
        articles = _get_articles_from_category(zim_archive, category_name)
        logger.info(f"Found {len(articles)} articles in category '{category_name}'")
        
        if not articles:
            logger.warning("No articles found")
            return
            
        # Test with first 3 articles
        test_articles = articles[:3]
        logger.info(f"Testing with first {len(test_articles)} articles")
        
        for article_title in test_articles:
            try:
                logger.info(f"Processing article: {article_title}")
                
                # Get the HTML content of the article
                html_content = article_html(zim_archive, article_title)
                
                if not html_content:
                    logger.warning(f"Could not retrieve HTML for article: {article_title}")
                    continue
                
                # Extract images from the article
                images = extract_images_from_article(html_content)
                logger.info(f"Found {len(images)} images in article")
                
                # Process chunks with image handling
                chunks = chunks_from_html(html_content)
                logger.info(f"Generated {len(chunks)} chunks")
                
                # Generate embeddings for chunks
                texts = [chunk['text'] for chunk in chunks]
                logger.info(f"Generating embeddings for {len(texts)} texts")
                vectors = embed_batch(texts)
                logger.info(f"Generated {len(vectors)} vectors")
                
                logger.info("About to call upload_batch with:")
                logger.info(f"  article_title: {article_title}")
                logger.info(f"  article_path: {article_title}")
                logger.info(f"  chunks length: {len(chunks)}")
                logger.info(f"  vectors length: {len(vectors)}")
                logger.info(f"  configuration_id(): {configuration_id()}")
                logger.info(f"  collection: TEST_COLLECTION")
                
                # This is where the error might occur
                upload_batch(
                    article_title=article_title,
                    article_path=article_title,  # Using title as path for single article
                    chunks=chunks,
                    vectors=vectors,        # Pass generated vectors
                    images=images,
                    configuration_id=configuration_id(),  # Call the function to get the ID
                    collection=TEST_COLLECTION,  # Use TEST_COLLECTION for import
                    generation_id=None,  # Will be set automatically
                )
                
                logger.info(f"Successfully processed article: {article_title}")
                
            except Exception as e:
                logger.error(f"Error processing article '{article_title}': {e}")
                import traceback
                traceback.print_exc()
                break
                
    except Exception as e:
        logger.error(f"Error in debug_import: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_import()