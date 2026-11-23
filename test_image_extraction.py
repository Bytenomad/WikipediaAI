#!/usr/bin/env python3
"""
Test script for image extraction functionality in Wikipedia AI pipeline.
"""

import os
import sys

# Add the src directory to the Python path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from wikipedia_ai.ingestion.image_extraction import extract_images_from_article
from wikipedia_ai.ingestion.chunking import process_article_with_images

def test_image_extraction():
    """Test image extraction with a simple HTML snippet"""
    print("Testing image extraction...")
    
    # Test with a simple HTML snippet to verify the image extraction works
    test_html = '''
    <html>
    <body>
    <div class="mw-parser-output">
    <img src="/wiki/File:Test_image.jpg" alt="Test Image" />
    <img src="/wiki/File:Another_image.png" alt="Another Image" />
    </div>
    </body>
    </html>
    '''

    images = extract_images_from_article(test_html, "https://en.wikipedia.org")
    print(f"Extracted {len(images)} images:")
    for img in images:
        print(f"  - {img}")
    
    return len(images) > 0

def test_full_article_processing():
    """Test full article processing with images"""
    print("\nTesting full article processing with images...")
    
    try:
        result = process_article_with_images("Medicine")
        if "error" in result:
            print(f"Error: {result['error']}")
            return False
        else:
            print(f"Processed article 'Medicine':")
            print(f"  Chunks: {result['total_chunks']}")
            print(f"  Images: {result['image_count']}")
            if result['images']:
                print("  First image:")
                print(f"    URL: {result['images'][0].get('url', 'N/A')}")
                print(f"    Alt text: {result['images'][0].get('alt', 'N/A')}")
            return True
    except Exception as e:
        print(f"Error during processing: {e}")
        return False

if __name__ == "__main__":
    print("Running image extraction tests...")
    
    test1_passed = test_image_extraction()
    test2_passed = test_full_article_processing()
    
    if test1_passed and test2_passed:
        print("\n[SUCCESS] All tests passed!")
    else:
        print("\n[FAILED] Some tests failed.")
        sys.exit(1)