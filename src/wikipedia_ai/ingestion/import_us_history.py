#!/usr/bin/env python3
"""
US History Wikipedia article import script.
This script imports articles from specific US history categories in batches to manage memory usage and processing time.
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
    # Use the correct approach that matches category_utils.py
    return _get_articles_from_category(zim_archive, category_name)


def import_us_history_category(category_name, batch_size=10):
    """
    Import all articles from a specific US history category in batches.
    
    Args:
        category_name: Name of the US history category to import
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
            
        logger.info(f"Starting import of {len(articles)} articles from US history category '{category_name}'")
        
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
            
            # Upload the batch to Qdrant
            if batch_data:
                try:
                    # Prepare the data for upload with proper parameters
                    # The upload_batch function expects a different signature than what was used
                    # Let's use the correct approach based on how import_category_batch.py works
                    
                    # Flatten chunks and images from all articles in this batch
                    all_chunks = []
                    all_images = []
                    all_titles = []
                    
                    for article in batch_data:
                        all_chunks.extend(article['chunks'])
                        all_images.extend(article['images'])
                        all_titles.append(article['title'])
                    
                    # Upload the batch with all articles together
                    upload_batch(
                        chunks=all_chunks,
                        images=all_images,
                        configuration_id=configuration_id,
                        collection=None,  # Will use default collection
                        generation_id=None,  # Will be set automatically
                        article_titles=all_titles  # Add article titles to help with identification
                    )
                    
                    logger.info(f"Successfully uploaded batch {i//batch_size + 1}")
                except Exception as e:
                    logger.error(f"Error uploading batch {i//batch_size + 1}: {e}")
            
        logger.info(f"Completed import of US history category '{category_name}'")
        
    except Exception as e:
        logger.error(f"Error in import_us_history_category: {e}")
        raise
    finally:
        # Ensure archive is closed
        if zim_archive and hasattr(zim_archive, 'close'):
            try:
                zim_archive.close()
            except Exception as e:
                logger.error(f"Error closing ZIM archive: {e}")

def main():
    """Main function to run the US history category import."""
    # Check for help flag
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        logger.info("Usage: python import_us_history.py <category_name> [batch_size]")
        logger.info("Example: python import_us_history.py 'United States' 5")
        logger.info("")
        logger.info("Imports US history Wikipedia articles from a specific category in batches.")
        logger.info("If batch_size is not provided, defaults to 10.")
        logger.info("")
        logger.info("Available US History Categories:")
        logger.info("  - United States")
        logger.info("  - History of the United States")
        logger.info("  - American Civil War")
        logger.info("  - American Revolution")
        logger.info("")
        logger.info("Important: Set ZIM_PATH environment variable to point to your Wikipedia ZIM file")
        return
         
    category_name = sys.argv[1]
    
    batch_size = 10
    if len(sys.argv) > 2:
        try:
            batch_size = int(sys.argv[2])
        except ValueError:
            logger.warning("Invalid batch size, using default of 10")
    
    import_us_history_category(category_name, batch_size)

if __name__ == "__main__":
    main()
