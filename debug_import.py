#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, '.')

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

# Test the function directly to see what's happening
def debug_import():
    try:
        print("Opening ZIM archive...")
        zim_archive = Archive(ZIM_PATH)
        
        print("Getting articles from category...")
        articles = _get_articles_from_category(zim_archive, "United States")
        print(f"Found {len(articles)} articles")
        
        if articles:
            article_title = articles[0]
            print(f"Processing article: {article_title}")
            print(f"Article title type: {type(article_title)}")
            
            # Get the HTML content of the article
            html_content = article_html(zim_archive, article_title)
            
            if not html_content:
                print("Could not retrieve HTML for article")
                return
            
            # Process chunks 
            chunks = chunks_from_html(html_content)
            print(f"Number of chunks: {len(chunks)}")
            
            # Generate embeddings
            if chunks:
                texts = [chunk['text'] for chunk in chunks]
                print(f"Generating embeddings for {len(texts)} texts")
                vectors = embed_batch(texts)
                print(f"Generated {len(vectors)} vectors")
                
                # Try to call upload_batch with debug info
                print("About to call upload_batch...")
                print(f"article_title type: {type(article_title)}")
                print(f"article_path type: {type(article_title)}")
                print(f"chunks length: {len(chunks)}")
                print(f"vectors length: {len(vectors)}")
                
                # This is where the error happens - let's test it
                upload_batch(
                    article_title=article_title,
                    article_path=article_title,  # Using title as path for single article
                    chunks=chunks,
                    vectors=vectors,
                    images=None,
                    configuration_id=configuration_id(),
                    collection=TEST_COLLECTION,
                    generation_id=None,
                )
                print("Upload successful!")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_import()