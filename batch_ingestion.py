#!/usr/bin/env python3
"""
Batched Wikipedia article ingestion script.
This script imports articles in batches to manage memory usage and processing time.
"""

import os
import sys
from typing import List, Optional
import logging

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wikipedia_ai.chunking import process_article
from wikipedia_ai.ingestion import run_full_ingestion, get_zim_file
from wikipedia_ai.qdrant_integration import create_qdrant_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def batch_import_articles(zim_path: str, batch_size: int = 100, start_index: int = 0, 
                         max_articles: Optional[int] = None, categories: Optional[List[str]] = None):
    """
    Import Wikipedia articles in batches.
    
    Args:
        zim_path (str): Path to the ZIM file
        batch_size (int): Number of articles to process per batch
        start_index (int): Starting index for article processing
        max_articles (int, optional): Maximum number of articles to process
        categories (List[str], optional): List of categories to filter by
    """
    
    logger.info(f"Starting batched import with batch size {batch_size}")
    
    # Get the ZIM file reader
    zim_file = get_zim_file(zim_path)
    
    if not zim_file:
        logger.error("Failed to open ZIM file")
        return
    
    try:
        # Get all article entries from ZIM
        articles = list(zim_file.iter_articles())
        
        total_articles = len(articles)
        logger.info(f"Found {total_articles} articles in ZIM file")
        
        if max_articles:
            total_articles = min(total_articles, max_articles)
            
        # Process articles in batches
        processed_count = 0
        
        for i in range(start_index, total_articles, batch_size):
            batch_end = min(i + batch_size, total_articles)
            batch_articles = articles[i:batch_end]
            
            logger.info(f"Processing batch {i//batch_size + 1}: articles {i} to {batch_end-1}")
            
            # Process this batch
            for article in batch_articles:
                try:
                    # Check if article matches categories filter if specified
                    if categories and not _article_matches_categories(article, categories):
                        continue
                    
                    # Process the article (this will handle chunking and Qdrant storage)
                    process_article(article)
                    processed_count += 1
                    
                except Exception as e:
                    logger.error(f"Error processing article {article.title}: {str(e)}")
                    continue
            
            logger.info(f"Completed batch {i//batch_size + 1}. Processed {processed_count} articles so far.")
            
            # Optional: Add a small delay between batches to prevent resource exhaustion
            # time.sleep(0.1)
        
        logger.info(f"Batch import completed. Total articles processed: {processed_count}")
        
    except Exception as e:
        logger.error(f"Error during batch import: {str(e)}")
        raise

def _article_matches_categories(article, categories):
    """
    Check if an article belongs to any of the specified categories.
    
    Args:
        article: ZIM article object
        categories (List[str]): List of category names to match against
        
    Returns:
        bool: True if article matches any category, False otherwise
    """
    # This is a simplified implementation - you'd need to adjust based on how 
    # your ZIM file stores category information
    try:
        article_title = article.title.lower()
        
        # Simple category matching logic - modify this based on your needs
        for category in categories:
            if category.lower() in article_title:
                return True
        return False
    except Exception:
        # If we can't determine category, default to including the article
        return True

def main():
    """Main function to run batched import."""
    
    # Configuration
    zim_path = "wikipedia/downloads/wikipedia_en_all_maxi_2026-08.zim"
    batch_size = 50  # Process 50 articles at a time
    max_articles = None  # Set to limit total articles, or None for all
    
    # Categories to import (optional)
    categories = None  # ["Medicine", "Technology", "History"]  # Uncomment to filter by categories
    
    logger.info("Starting batched Wikipedia import")
    
    try:
        batch_import_articles(
            zim_path=zim_path,
            batch_size=batch_size,
            max_articles=max_articles,
            categories=categories
        )
        
        logger.info("Batch import completed successfully!")
        
    except Exception as e:
        logger.error(f"Batch import failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()