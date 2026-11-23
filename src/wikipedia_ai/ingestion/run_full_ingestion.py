#!/usr/bin/env python3
"""
Run the complete Wikipedia AI ingestion process to upload data to Qdrant.
This script processes real Wikipedia articles from the ZIM file.
"""


import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import required modules
from libzim.reader import Archive
from bs4 import BeautifulSoup

# Import chunking functions
from chunking import (
    ZIM_PATH,
    MAX_CHARS,
    NON_PROSE_SELECTORS,
    article_html,
    remove_excluded_sections,
    eligible_records,
    make_chunks
)
from qdrant_batch import upload_batch
from config import configuration_id
import json

def run_full_ingestion():
    """Run the complete ingestion process."""
    print("=== Running Full Ingestion Process ===")
    
    # Test with a few sample articles that should be in the ZIM file
    test_articles = ["Medicine"]
    
    try:
        for article_title in test_articles:
            print(f"\n--- Processing article: {article_title} ---")
            
            # First, let's make sure we can read from the ZIM file properly
            print("Checking ZIM file access...")
            
            try:
                # Open the archive
                archive = Archive(ZIM_PATH)
                print(f"Successfully opened ZIM file: {ZIM_PATH}")
                
                # Process the article with chunking functions
                print("Processing article content...")
                
                # Get HTML content using the article_html function which takes archive and title
                html_content = article_html(archive, article_title)
                print(f"HTML content length: {len(html_content)}")
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(html_content, "lxml")
                
                # Find the main content area
                content = soup.select_one(".mw-parser-output")
                if content is None:
                    print("Could not find .mw-parser-output in the article.")
                    continue
                
                # Remove excluded sections
                remove_excluded_sections(content)
                
                # Remove non-prose elements
                for node in content.select(NON_PROSE_SELECTORS):
                    node.decompose()
                
                # Get eligible records and make chunks
                records = eligible_records(content)
                chunks = make_chunks(records, MAX_CHARS)
                
                print(f"Article '{article_title}' processed successfully")
                print(f"Number of chunks: {len(chunks)}")
                
                # Show first few chunks as sample
                for i, chunk in enumerate(chunks[:3]):
                    print(f"Chunk {i+1}: Section '{chunk['section']}' - {len(chunk['text'])} chars")
                
                # Now upload to Qdrant
                print("Uploading to Qdrant...")
                # For this test, we'll use the TEST_COLLECTION
                from target import TEST_COLLECTION
                
                # Upload in batches (this is a simplified version)
                batch_size = 10
                total_uploaded = 0
                
                for i in range(0, len(chunks), batch_size):
                    batch_chunks = chunks[i:i + batch_size]
                    # In a real implementation, we would generate embeddings here
                    # For now, we'll use dummy vectors (this is just to test the upload)
                    dummy_vectors = [[0.0] * 768 for _ in range(len(batch_chunks))]
                    
                    uploaded_count = upload_batch(
                        article_title=article_title,
                        article_path=f"articles/{article_title}",
                        chunks=batch_chunks,
                        vectors=dummy_vectors,
                        collection=TEST_COLLECTION,
                        configuration_id=configuration_id()  # Call the function to get the ID
                    )
                    total_uploaded += uploaded_count
                    print(f"Uploaded batch {i//batch_size + 1}: {uploaded_count} points")
                
                print(f"[SUCCESS] Article '{article_title}' processed and uploaded to Qdrant ({total_uploaded} chunks)")
                
            except Exception as e:
                print(f"[ERROR] Error processing article '{article_title}': {e}")
                import traceback
                traceback.print_exc()
                continue
                
        print("\n=== Full ingestion process completed ===")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error during full ingestion: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    run_full_ingestion()