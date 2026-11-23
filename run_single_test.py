#!/usr/bin/env python3
"""Run a single article test to verify the pipeline works."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from wikipedia_ai.ingestion.article_ingestion import ingest_article

def main():
    print("=== Wikipedia AI Single Article Test ===")
    
    # Test with a simple title that we know exists in Wikipedia
    test_articles = [
        "Testville",  # Our test article
        "Artificial intelligence",  # A real Wikipedia article for testing
    ]
    
    for article_title in test_articles:
        print(f"\n--- Testing article: {article_title} ---")
        try:
            result = ingest_article(article_title)
            print(f"SUCCESS: {article_title} - Result: {result}")
        except Exception as e:
            print(f"ERROR with {article_title}: {e}")
            # Continue with other articles
            continue
    
    print("\n=== Test completed ===")

if __name__ == "__main__":
    main()