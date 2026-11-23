#!/usr/bin/env python3
"""
Test script to validate US history import functionality.
This script tests the category access and article retrieval functions.
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

# Import configuration
from wikipedia_ai.ingestion.chunking import ZIM_PATH

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_category_access():
    """Test that we can properly access categories in the ZIM file."""
    logger.info(f"Testing category access with ZIM_PATH: {ZIM_PATH}")
    
    try:
        # Open the ZIM archive
        logger.info("Opening ZIM archive...")
        zim_archive = Archive(ZIM_PATH)
        logger.info("ZIM archive opened successfully")
        
        # Test accessing specific categories that should exist in US history
        test_categories = [
            "Category:United States",
            "Category:History of the United States", 
            "Category:American Civil War",
            "Category:American Revolution"
        ]
        
        for category_name in test_categories:
            logger.info(f"Testing access to category: {category_name}")
            
            # Test using the proper method from category_utils
            try:
                articles = _get_articles_from_category(zim_archive, category_name)
                logger.info(f"Found {len(articles)} articles in category '{category_name}'")
                
                if articles:
                    logger.info(f"First few articles: {articles[:3]}")
                else:
                    logger.warning(f"No articles found in category '{category_name}'")
                    
            except Exception as e:
                logger.error(f"Error accessing category '{category_name}': {e}")
                
        # Also test with the more generic approach
        logger.info("Testing with generic approach...")
        for category_name in ["United States", "History of the United States"]:
            try:
                articles = _get_articles_from_category(zim_archive, category_name)
                logger.info(f"Found {len(articles)} articles in category '{category_name}'")
                
                if articles:
                    logger.info(f"First few articles: {articles[:3]}")
                    
            except Exception as e:
                logger.error(f"Error accessing category '{category_name}': {e}")
                
    except Exception as e:
        logger.error(f"Error opening ZIM archive: {e}")
        return False
        
    return True

def test_zim_file_structure():
    """Test basic ZIM file structure to understand how categories work."""
    logger.info("Testing ZIM file structure...")
    
    try:
        zim_archive = Archive(ZIM_PATH)
        
        # Get some information about the archive
        logger.info(f"Archive title: {zim_archive.get_title()}")
        logger.info(f"Archive language: {zim_archive.get_language()}")
        logger.info(f"Archive number of items: {zim_archive.get_number_of_entries()}")
        
        # Try to search for some entries that might be categories
        logger.info("Searching for category entries...")
        
        # Test with a simple search approach
        try:
            # This is a more direct way to check if we can access entries by title
            test_titles = ["Category:United States", "Category:History of the United States"]
            
            for title in test_titles:
                try:
                    entry = zim_archive.get_entry_by_title(title)
                    logger.info(f"Found entry for '{title}'")
                    
                    item = entry.get_item()
                    logger.info(f"Entry type: {item.mimetype}")
                    
                except Exception as e:
                    logger.warning(f"Could not find entry for '{title}': {e}")
                    
        except Exception as e:
            logger.error(f"Error searching entries: {e}")
            
    except Exception as e:
        logger.error(f"Error in test_zim_file_structure: {e}")
        return False
        
    return True

if __name__ == "__main__":
    logger.info("Starting US History Import Test")
    
    success = True
    success &= test_category_access()
    success &= test_zim_file_structure()
    
    if success:
        logger.info("All tests passed!")
    else:
        logger.error("Some tests failed!")
        
    sys.exit(0 if success else 1)