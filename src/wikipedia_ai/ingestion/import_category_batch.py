#!/usr/bin/env python3
"""
Category-based Wikipedia article import script.
This script imports articles from specific categories in batches to manage memory usage and processing time.
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

def get_articles_from_category(zim_archive, category_name):
    """Return direct article members using the shared ZIM category parser."""
    return _get_articles_from_category(zim_archive, category_name)


def import_category_batch(category_name, batch_size=10):
    """
    Import all articles from a specific category in batches.
    
    Args:
        category_name: Name of the category to import
        batch_size: Number of articles to process in each batch
    """
    zim_archive = None
    try:
        # Open the ZIM archive
        logger.info(f"Opening ZIM archive at {ZIM_PATH}")
        zim_archive = Archive(ZIM_PATH)
        
        # Get all articles from the specified category
        articles = get_articles_from_category(zim_archive, category_name)
        
        if not articles:
            logger.warning(f"No articles found in category '{category_name}'")
            return
            
        logger.info(f"Starting import of {len(articles)} articles from category '{category_name}'")
        
        # Process articles in batches
        for i in range(0, len(articles), batch_size):
            batch = articles[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1} with {len(batch)} articles")
            
            # Collect article data for this batch
            batch_data = []
            
            for article_title in batch:
                try:
                    # Get the HTML content of the article
                    html_content = article_html(zim_archive, article_title)
                    
                    if not html_content:
                        logger.warning(f"Could not retrieve HTML for article: {article_title}")
                        continue
                    
                    # Extract images from the article
                    images = extract_images_from_article(html_content)
                    
                    # Process chunks with image handling
                    chunks = chunks_from_html(html_content)
                    
                    # Format response with images for Open WebUI display
                    formatted_response = format_response_with_images(chunks, images)
                    
                    batch_data.append({
                        'title': article_title,
                        'chunks': chunks,
                        'images': images,
                        'formatted_response': formatted_response
                    })
                    
                except Exception as e:
                    logger.error(f"Error processing article '{article_title}': {e}")
                    continue
            
            # Upload the batch to Qdrant - one article at a time
            if batch_data:
                try:
                    for article in batch_data:
                        upload_batch(
                            article_title=article['title'],
                            article_path=article['title'],  # Using title as path for single article
                            chunks=article['chunks'],
                            vectors=None,        # Vectors are generated during upload
                            collection=None,     # Will use default collection
                            configuration_id=configuration_id,
                            generation_id=None,  # Will be set automatically
                            images=article['images']
                        )
                    logger.info(f"Successfully uploaded batch {i//batch_size + 1}")
                except Exception as e:
                    logger.error(f"Error uploading batch {i//batch_size + 1}: {e}")
            
        logger.info(f"Completed import of category '{category_name}'")
        
    except Exception as e:
        logger.error(f"Error in import_category_batch: {e}")
        raise

def main():
    """Main function to run the category import."""
    # Check for help flag
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        logger.info("Usage: python import_category_batch.py <category_name> [batch_size]")
        logger.info("Example: python import_category_batch.py 'Medicine' 5")
        logger.info("")
        logger.info("Imports Wikipedia articles from a specific category in batches.")
        logger.info("If batch_size is not provided, defaults to 10.")
        logger.info("")
        logger.info("Available options:")
        logger.info("  -h, --help     Show this help message and exit")
        return
        
    category_name = sys.argv[1]
    
    batch_size = 10
    if len(sys.argv) > 2:
        try:
            batch_size = int(sys.argv[2])
        except ValueError:
            logger.warning("Invalid batch size, using default of 10")
    
    import_category_batch(category_name, batch_size)

if __name__ == "__main__":
    main()
