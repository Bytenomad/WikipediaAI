#!/usr/bin/env python3
"""
Test script for image extraction functionality.
"""

import _bootstrap

import sys
sys.path.insert(0, 'src')

from wikipedia_ai.ingestion.image_extraction import extract_images_from_article

# Create simple test HTML with images
test_html = '<html><body><h1>Test Article</h1><p>This is a sample article.</p><img src="/wiki/File:Sample.jpg" alt="Sample Image"><img src="/wiki/File:Another.png" alt="Another Image"></body></html>'

try:
    images = extract_images_from_article(test_html)
    print('OK: Image extraction works correctly')
    print(f'Found {len(images)} images')
    
    if images:
        for img in images:
            print(f'  - URL: {img["url"]}')
            print(f'  - Alt text: {img["alt"]}')
            print(f'  - Filename: {img["filename"]}')
            
except Exception as e:
    print(f'ERROR: Image extraction failed: {e}')
    import traceback
    traceback.print_exc()
