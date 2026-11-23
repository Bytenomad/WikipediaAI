#!/usr/bin/env python3
"""
Import a batch of articles from a specific category.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__) + '/src')

from wikipedia_ai.ingestion.batched_ingestion_robust import process_article_batch
from wikipedia_ai.ingestion.chunking import ZIM_PATH

def import_category_articles(category_name):
    """Import articles from a specific category."""
    
    # Define your article list for this category
    # This could be read from a file or generated programmatically
    if category_name == "Medicine":
        articles = [
            "Medicine",
            "Healthcare",
            "Disease",
            "Treatment",
            "Diagnosis",
            "Pharmacology",
            "Surgery",
            "Pediatrics",
            "Geriatrics"
        ]
    elif category_name == "Science":
        articles = [
            "Science",
            "Physics",
            "Chemistry",
            "Biology",
            "Astronomy",
            "Geology",
            "Ecology",
            "Genetics"
        ]
    elif category_name == "History":
        articles = [
            "History",
            "Ancient_history",
            "Medieval_history",
            "Modern_history",
            "World_war",
            "Revolution",
            "Empire",
            "Civilization"
        ]
    else:
        # Default fallback - you can customize this
        articles = [
            "Artificial_intelligence",
            "Machine_learning",
            "Data_science",
            "Computer_science",
            "Software_engineering"
        ]
    
    print(f"Importing {len(articles)} articles from category: {category_name}")
    
    try:
        # Process the batch
        result = process_article_batch(articles)
        print(f"✅ Successfully imported {len(articles)} articles")
        return True
        
    except Exception as e:
        print(f"❌ Error importing articles: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # You can specify which category to import
    category = "Medicine"  # Default category
    
    if len(sys.argv) > 1:
        category = sys.argv[1]
    
    import_category_articles(category)