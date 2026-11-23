#!/usr/bin/env python3
"""
Test script to run a single article ingestion test.
This will help us understand how the pipeline works with actual data.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from wikipedia_ai.ingestion.article_ingestion import ingest_article

def main():
    print("=== Wikipedia AI Single Article Ingestion Test ===")
    
    # Test with a simple title that we know exists in Wikipedia
    test_articles = [
        "Testville",  # Our test article
        "Artificial intelligence",  # A real Wikipedia article for testing
        "Machine learning",  # Another real Wikipedia article
    ]
    
    print("Testing ingestion process...")
    
    for article_title in test_articles:
        print(f"\n--- Testing article: {article_title} ---")
        try:
            result = ingest_article(article_title)
            print(f"SUCCESS: {article_title} - Result: {result}")
            
            # In a real scenario, we'd want to check if data was actually stored
            print("Ingestion would normally store data in Qdrant database")
            
        except Exception as e:
            print(f"ERROR with {article_title}: {e}")
            # Continue with other articles
            continue
    
    print("\n=== Test completed ===")

if __name__ == "__main__":
    main()