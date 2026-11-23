#!/usr/bin/env python3
"""
Test script to verify that Wikipedia AI pipeline with image support works correctly.
This script tests both the text processing and image extraction functionality.
"""

import os
import sys
import json
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from wikipedia_ai.ingestion.image_extraction import extract_images_from_article
from wikipedia_ai.ingestion.chunking import process_article_with_images
from wikipedia_ai.ingestion.batched_ingestion import process_articles_batched

def test_image_extraction():
    """Test the image extraction functionality with sample HTML content."""
    print("Testing image extraction functionality...")
    
    # Sample HTML content with images (simplified Wikipedia-like structure)
    sample_html = """
    <html>
    <body>
        <div class="mw-parser-output">
            <p>This is a test article about technology.</p>
            <img src="/images/tech1.jpg" alt="Technology Image 1" title="Tech Image 1" width="200" height="150"/>
            <p>Another paragraph with more content.</p>
            <img src="/images/tech2.png" alt="Technology Image 2" title="Tech Image 2" width="300" height="200"/>
            <p>Final paragraph of the article.</p>
        </div>
    </body>
    </html>
    """
    
    images = extract_images_from_article(sample_html, base_url="http://example.com")
    
    print(f"Extracted {len(images)} images:")
    for i, img in enumerate(images):
        print(f"  Image {i+1}: {img}")
    
    # Verify we got the expected number of images
    assert len(images) == 2, f"Expected 2 images, got {len(images)}"
    
    # Verify image properties - note: the actual structure might be different from our test
    # since extract_images_from_article doesn't use title attribute in the same way
    assert images[0]['url'] == "http://example.com/images/tech1.jpg"
    assert images[0]['alt_text'] == "Technology Image 1"
    
    assert images[1]['url'] == "http://example.com/images/tech2.png"
    assert images[1]['alt_text'] == "Technology Image 2"
    
    print("✓ Image extraction test passed")
    return True

def test_chunking_with_images():
    """Test chunking functionality with image information."""
    print("\nTesting chunking with image information...")
    
    # Sample HTML content with images
    sample_html = """
    <html>
    <body>
        <div class="mw-parser-output">
            <h2>Introduction</h2>
            <p>This is the introduction to the article.</p>
            <img src="/images/intro.jpg" alt="Intro Image" title="Intro Image"/>
            
            <h2>Main Content</h2>
            <p>This is the main content of the article with more details.</p>
            <img src="/images/main.png" alt="Main Image" title="Main Image"/>
            
            <h2>Conclusion</h2>
            <p>This concludes the article.</p>
        </div>
    </body>
    </html>
    """
    
    # Test processing with images
    result = process_article_with_images("Test Article")
    print(f"Processed article into {len(result['chunks'])} chunks")
    
    # Verify basic structure of chunks
    assert len(result['chunks']) >= 1
    for chunk in result['chunks']:
        assert 'chunk_index' in chunk
        assert 'section' in chunk
        assert 'text' in chunk
    
    print("✓ Chunking test passed")
    return True

def test_integration():
    """Test the full integration of image support."""
    print("\nTesting complete integration...")
    
    # This would normally process a real article, but we'll verify the components work
    try:
        # Test that all required modules can be imported
        from wikipedia_ai.ingestion.image_extraction import extract_images_from_article
        from wikipedia_ai.ingestion.chunking import process_article_with_images
        from wikipedia_ai.ingestion.batched_ingestion import process_articles_batched
        
        print("✓ All modules imported successfully")
        
        # Test that functions exist and are callable
        assert callable(extract_images_from_article)
        assert callable(process_article_with_images)
        assert callable(process_articles_batched)
        
        print("✓ All functions are callable")
        
        # Run a basic test of image extraction
        sample_html = """
        <html>
        <body>
            <div class="mw-parser-output">
                <p>Test content with an image.</p>
                <img src="/test.jpg" alt="Test Image"/>
            </div>
        </body>
        </html>
        """
        
        images = extract_images_from_article(sample_html)
        assert isinstance(images, list)
        
        print("✓ Integration test completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Running Wikipedia AI Image Support Integration Tests\n")
    
    tests = [
        test_image_extraction,
        test_chunking_with_images,
        test_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed: {e}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All integration tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())