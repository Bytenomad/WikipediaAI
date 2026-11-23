#!/usr/bin/env python3
"""
Import all US History Wikipedia articles from multiple categories.
This script imports articles from all major US history categories in batches.
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

# Define US history categories to import
US_HISTORY_CATEGORIES = [
    "United States",
    "History of the United States", 
    "American Civil War",
    "American Revolution"
]

def get_articles_from_category(zim_archive, category_name):
    """Return direct article members using the shared ZIM category parser."""
    return _get_articles_from_category(zim_archive, category_name)


def import_all_us_history_categories(batch_size=10):
    """
    Import all articles from all US history categories in batches.
    
    Args:
        batch_size: Number of articles to process in each batch
    """
    try:
        # Open the ZIM archive
        logger.info(f"Opening ZIM archive at {ZIM_PATH}")
        zim_archive = Archive(ZIM_PATH)
        
        all_articles = []
        
        # Get all articles from each US history category
        for category_name in US_HISTORY_CATEGORIES:
            logger.info(f"Retrieving articles from category: {category_name}")
            articles = get_articles_from_category(zim_archive, category_name)
            all_articles.extend(articles)
            logger.info(f"Found {len(articles)} articles in category '{category_name}'")
        
        if not all_articles:
            logger.warning("No articles found in any US history category")
            return
            
        # Remove duplicates while preserving order
        unique_articles = list(dict.fromkeys(all_articles))  # Preserve order and remove duplicates
        logger.info(f"Total unique articles to import: {len(unique_articles)}")
        
        # Process articles in batches across all categories
        for i in range(0, len(unique_articles), batch_size):
            batch = unique_articles[i:i + batch_size]
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
                        # Generate embeddings for chunks
                        vectors = embed_batch([chunk['text'] for chunk in article['chunks']])
                        
                        logger.debug(f"About to upload article: {article['title']}")
                        logger.debug(f"Article title type: {type(article['title'])}")
                        logger.debug(f"Article chunks length: {len(article['chunks'])}")
                        logger.debug(f"Vectors length: {len(vectors)}")
                        
                        # Process chunks in smaller batches to avoid exceeding BATCH_SIZE limit
                        CHUNK_BATCH_SIZE = 32
                        article_images = article['images']  # Store images once
                        for i in range(0, len(article['chunks']), CHUNK_BATCH_SIZE):
                            batch_chunks = article['chunks'][i:i + CHUNK_BATCH_SIZE]
                            batch_vectors = vectors[i:i + CHUNK_BATCH_SIZE]
                            
                            # Ensure we have the same number of chunks and vectors
                            if len(batch_chunks) != len(batch_vectors):
                                raise ValueError("Mismatch between chunks and vectors in batch")
                                
                            upload_batch(
                                article_title=article['title'],
                                article_path=str(article['title']),  # Using title as path for single article, ensure it's a string
                                chunks=batch_chunks,
                                vectors=batch_vectors,        # Pass generated vectors
                                images=article_images if i == 0 else None,  # Only pass images once
                                configuration_id=configuration_id(),  # Call the function to get the ID
                                collection=TEST_COLLECTION,  # Use TEST_COLLECTION for import
                                generation_id=None,  # Will be set automatically
                            )
                    logger.info(f"Successfully uploaded batch {i//batch_size + 1}")
                except Exception as e:
                    logger.error(f"Error uploading batch {i//batch_size + 1}: {e}")
                    raise  # Re-raise the exception to see full traceback
            
        logger.info("Completed import of all US history categories")
        
    except Exception as e:
        logger.error(f"Error in import_all_us_history_categories: {e}")
        raise

def main():
    """Main function to run the US history import."""
    # Check for help flag
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        logger.info("Usage: python import_all_us_history.py [batch_size]")
        logger.info("Example: python import_all_us_history.py 5")
        logger.info("")
        logger.info("Imports all US history Wikipedia articles from multiple categories in batches.")
        logger.info("If batch_size is not provided, defaults to 10.")
        logger.info("")
        logger.info("US History Categories to Import:")
        for category in US_HISTORY_CATEGORIES:
            logger.info(f"  - {category}")
        logger.info("")
        logger.info("Important: Set ZIM_PATH environment variable to point to your Wikipedia ZIM file")
        return
         
    batch_size = 10
    if len(sys.argv) > 1:
        try:
            batch_size = int(sys.argv[1])
        except ValueError:
            logger.warning("Invalid batch size, using default of 10")
    
    import_all_us_history_categories(batch_size)

if __name__ == "__main__":
    main()
