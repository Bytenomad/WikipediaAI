#!/usr/bin/env python3
"""
Batched Wikipedia article ingestion script.
This script imports articles in batches to manage memory usage and processing time.
"""

import sys
import os
from pathlib import Path

# Add the parent directory (src) to Python path so modules can be imported properly
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import required modules
from libzim.reader import Archive
from bs4 import BeautifulSoup

# Import chunking functions
from wikipedia_ai.ingestion.chunking import (
    ZIM_PATH,
    MAX_CHARS,
    NON_PROSE_SELECTORS,
    article_html,
    remove_excluded_sections,
    eligible_records,
    make_chunks
)
from wikipedia_ai.ingestion.qdrant_batch import upload_batch
from wikipedia_ai.ingestion.config import configuration_id
import json

# Import image extraction functionality
from wikipedia_ai.ingestion.image_extraction import extract_images_from_article

def process_article_batch(archive: Archive, article_titles: list, collection_name: str, batch_size: int = 50):
    """
    Process a batch of articles and upload to Qdrant.
    
    Args:
        archive (Archive): Open ZIM archive
        article_titles (list): List of article titles to process
        collection_name (str): Qdrant collection name
        batch_size (int): Size of chunks to process at once
    
    Returns:
        int: Total number of chunks processed
    """
    total_chunks = 0
    
    for i, article_title in enumerate(article_titles):
        print(f"Processing article {i+1}/{len(article_titles)}: {article_title}")
        
        try:
            # Process the article with chunking functions
            html_content = article_html(archive, article_title)
            
            if not html_content:
                print(f"  Warning: No content found for article '{article_title}'")
                continue
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(html_content, "lxml")
            
            # Find the main content area
            content = soup.select_one(".mw-parser-output")
            if content is None:
                print(f"  Warning: Could not find .mw-parser-output in article '{article_title}'")
                continue
            
            # Remove excluded sections
            remove_excluded_sections(content)
            
            # Remove non-prose elements
            for node in content.select(NON_PROSE_SELECTORS):
                node.decompose()
            
            # Get eligible records and make chunks
            records = eligible_records(content)
            chunks = make_chunks(records, MAX_CHARS)
            
            # Extract image information from the article
            images = extract_images_from_article(html_content, "https://en.wikipedia.org")
            
            print(f"  Article '{article_title}' processed successfully")
            print(f"  Number of chunks: {len(chunks)}")
            print(f"  Number of images: {len(images)}")
            
            # Upload to Qdrant in smaller batches
            if chunks:
                upload_count = 0
                for j in range(0, len(chunks), batch_size):
                    batch_chunks = chunks[j:j + batch_size]
                    
                    # For this demo, we'll use dummy vectors (in real implementation, 
                    # you'd generate actual embeddings)
                    dummy_vectors = [[0.0] * 768 for _ in range(len(batch_chunks))]
                    
                    # Prepare image data for this batch - match the number of chunks
                    batch_images = []
                    if images:
                        # If we have more images than chunks, truncate or pad as needed
                        # For now, just match the number of chunks (this is a simplification)
                        batch_images = images[:len(batch_chunks)] if len(images) >= len(batch_chunks) else images + [None] * (len(batch_chunks) - len(images))
                    
                    # For active collection, we need a generation_id
                    if collection_name == "wikipedia_articles":
                        generation_id = "batch_1"
                    else:
                        generation_id = None
                    
                    uploaded_count = upload_batch(
                        article_title=article_title,
                        article_path=f"articles/{article_title}",
                        chunks=batch_chunks,
                        vectors=dummy_vectors,
                        collection=collection_name,
                        configuration_id=configuration_id(),  # Call the function to get the ID
                        generation_id=generation_id,
                        images=batch_images  # Pass image information along with chunks
                    )
                    upload_count += uploaded_count
                    print(f"    Uploaded batch {j//batch_size + 1}: {uploaded_count} points")
                
                total_chunks += upload_count
                print(f"  Total chunks uploaded for '{article_title}': {upload_count}")
            
        except Exception as e:
            print(f"  Error processing article '{article_title}': {e}")
            import traceback
            traceback.print_exc()
            continue
    
    return total_chunks

def run_batched_ingestion(article_list_file: str = None, batch_size: int = 50, 
                         collection_name: str = "wikipedia_test_articles"):
    """
    Run the complete batched ingestion process.
    
    Args:
        article_list_file (str): Path to file containing list of articles (one per line)
        batch_size (int): Size of batches for processing
        collection_name (str): Qdrant collection name to use
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("=== Running Batched Ingestion Process ===")
    
    try:
        # Open the archive
        print(f"Opening ZIM file: {ZIM_PATH}")
        archive = Archive(ZIM_PATH)
        print("Successfully opened ZIM file")
        
        # Get list of articles to process
        if article_list_file and os.path.exists(article_list_file):
            # Read from file
            with open(article_list_file, 'r') as f:
                article_titles = [line.strip() for line in f if line.strip()]
            print(f"Processing {len(article_titles)} articles from file: {article_list_file}")
        else:
            # Use default test articles
            article_titles = ["Medicine", "Technology", "History"]
            print("Processing default test articles")
        
        total_chunks = 0
        
        # Process in batches of specified size
        for i in range(0, len(article_titles), batch_size):
            batch_articles = article_titles[i:i + batch_size]
            print(f"\n--- Processing batch {i//batch_size + 1} ---")
            
            chunks_in_batch = process_article_batch(archive, batch_articles, collection_name, batch_size)
            total_chunks += chunks_in_batch
            
            print(f"Batch {i//batch_size + 1} completed. Chunks in this batch: {chunks_in_batch}")
        
        print(f"\n=== Batched ingestion completed ===")
        print(f"Total articles processed: {len(article_titles)}")
        print(f"Total chunks uploaded: {total_chunks}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error during batched ingestion: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Batched Wikipedia ingestion')
    parser.add_argument('--article-list-file', type=str, help='Path to file containing list of articles (one per line)')
    parser.add_argument('--batch-size', type=int, default=20, help='Size of batches for processing')
    parser.add_argument('--collection-name', type=str, default="wikipedia_test_articles", help='Qdrant collection name to use')
    
    args = parser.parse_args()
    
    # Default parameters
    article_list_file = args.article_list_file
    batch_size = args.batch_size
    collection_name = args.collection_name
    
    print("Starting batched Wikipedia ingestion...")
    print(f"Article list file: {article_list_file}")
    print(f"Batch size: {batch_size}")
    print(f"Collection name: {collection_name}")
    
    try:
        success = run_batched_ingestion(article_list_file, batch_size, collection_name)
        
        if success:
            print("Batched ingestion completed successfully!")
        else:
            print("Batched ingestion failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"Batched ingestion failed with error: {e}")
        sys.exit(1)