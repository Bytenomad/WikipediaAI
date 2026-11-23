#!/usr/bin/env python3

import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from wikipedia_ai.ingestion.chunking import chunks_from_html, article_html
from wikipedia_ai.ingestion.batch_embeddings import embed_batch
from wikipedia_ai.ingestion.qdrant_batch import upload_batch
from wikipedia_ai.ingestion.config import configuration_id
from wikipedia_ai.ingestion.target import TEST_COLLECTION

# Test with a simple article to debug the issue
import logging
logging.basicConfig(level=logging.DEBUG)

try:
    # Simulate what happens in the main script
    from libzim.reader import Archive
    ZIM_PATH = "D:/WikipediaAI/wikipedia/downloads/wikipedia_en_all_maxi_2026-08.zim"
    
    zim_archive = Archive(ZIM_PATH)
    
    article_title = "United States"  # Using a simple title that should exist
    
    print(f"Processing article: {article_title}")
    
    # Get the HTML content of the article
    html_content = article_html(zim_archive, article_title)
    
    if not html_content:
        print("Could not retrieve HTML for article")
        sys.exit(1)
    
    print("Got HTML content, extracting chunks...")
    
    # Process chunks 
    chunks = chunks_from_html(html_content)
    
    print(f"Extracted {len(chunks)} chunks")
    
    if chunks:
        print(f"First chunk: section='{chunks[0]['section']}', text length={len(chunks[0]['text'])}")
        
        # Generate embeddings for chunks
        texts_for_embedding = [chunk['text'] for chunk in chunks]
        print(f"Texts for embedding: {len(texts_for_embedding)}")
        
        vectors = embed_batch(texts_for_embedding)
        print(f"Generated {len(vectors)} vectors")
        
        print("About to call upload_batch...")
        # Test the upload_batch with minimal data
        try:
            # Let's also add some debugging to see what exactly is passed to upload_batch
            print(f"article_title type: {type(article_title)}")
            print(f"article_path type: {type(article_title)}")  # Using title as path for single article
            print(f"chunks type: {type(chunks)}")
            print(f"vectors type: {type(vectors)}")
            print(f"images type: {type([])}")  # Empty images list
            print(f"configuration_id() type: {type(configuration_id())}")
            print(f"collection type: {type(TEST_COLLECTION)}")
            
            upload_batch(
                article_title=article_title,
                article_path=article_title,  # Using title as path for single article
                chunks=chunks,
                vectors=vectors,        # Pass generated vectors
                images=[],              # Empty images list
                configuration_id=configuration_id(),  # Call the function to get the ID
                collection=TEST_COLLECTION,  # Use TEST_COLLECTION for import
                generation_id=None,  # Will be set automatically
            )
            print("Upload successful!")
        except Exception as e:
            print(f"Error in upload_batch: {e}")
            import traceback
            traceback.print_exc()
    
except Exception as e:
    print(f"Error in debug script: {e}")
    import traceback
    traceback.print_exc()