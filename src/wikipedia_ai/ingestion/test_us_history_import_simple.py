#!/usr/bin/env python3
"""
Simple test to validate US history import functionality.
This script tests that we can properly run a small import from one of the US history categories.
"""

import sys
import os
from pathlib import Path

# Add the parent directory (src) to Python path so modules can be imported properly
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import required modules for testing
from libzim.reader import Archive
from wikipedia_ai.ingestion.category_utils import get_articles_from_category as _get_articles_from_category

# Import configuration
from wikipedia_ai.ingestion.chunking import ZIM_PATH

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_basic_import_functionality():
    """Test basic functionality of importing from a US history category."""
    logger.info(f"Testing import functionality with ZIM_PATH: {ZIM_PATH}")
    
    try:
        # Open the ZIM archive
        logger.info("Opening ZIM archive...")
        zim_archive = Archive(ZIM_PATH)
        logger.info("ZIM archive opened successfully")
        
        # Test accessing one of the US history categories
        category_name = "Category:United States"
        logger.info(f"Testing access to category: {category_name}")
        
        # Test using the proper method from category_utils
        articles = _get_articles_from_category(zim_archive, category_name)
        logger.info(f"Found {len(articles)} articles in category '{category_name}'")
        
        if articles:
            logger.info(f"First few articles: {articles[:3]}")
            
            # Test that we can process at least one article
            first_article = articles[0]
            logger.info(f"Testing processing of article: {first_article}")
            
            # This is a basic test - just verify we can get the article content
            try:
                from wikipedia_ai.ingestion.chunking import article_html
                html_content = article_html(first_article)
                if html_content:
                    logger.info(f"Successfully retrieved HTML for '{first_article}' (length: {len(html_content)} chars)")
                else:
                    logger.warning(f"No HTML content found for '{first_article}'")
                    
            except Exception as e:
                logger.error(f"Error retrieving HTML for article '{first_article}': {e}")
                
        else:
            logger.warning(f"No articles found in category '{category_name}'")
            
    except Exception as e:
        logger.error(f"Error in test_basic_import_functionality: {e}")
        return False
        
    return True

if __name__ == "__main__":
    logger.info("Starting Basic US History Import Test")
    
    success = test_basic_import_functionality()
    
    if success:
        logger.info("Basic import functionality test passed!")
    else:
        logger.error("Basic import functionality test failed!")
        
    sys.exit(0 if success else 1)