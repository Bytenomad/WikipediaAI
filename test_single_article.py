#!/usr/bin/env python3
"""Test script to process a single article and prepare it for Open WebUI chat."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from wikipedia_ai.ingestion.article_ingestion import ingest_article

def test_single_article():
    """Process a single test article."""
    
    # Create a simple test article title
    article_title = "Testville"
    
    print("Starting single article test...")
    print(f"Processing article: {article_title}")
    
    try:
        result = ingest_article(article_title)
        print(f"Ingestion result: {result}")
        return True
    except Exception as e:
        print(f"Error during ingestion: {e}")
        return False

if __name__ == "__main__":
    test_single_article()