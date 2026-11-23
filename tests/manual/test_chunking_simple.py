#!/usr/bin/env python3
"""
Simple test to verify that the chunking functionality works correctly.
"""

import _bootstrap

import sys
import os
sys.path.insert(0, 'src')

def test_chunking_functionality():
    """Test that we can properly chunk Wikipedia articles."""
    print("Testing chunking functionality...")
    
    try:
        # Import required functions
        from wikipedia_ai.ingestion.chunking import (
            ZIM_PATH, 
            ARTICLE_TITLE, 
            MAX_CHARS,
            article_html,
            eligible_records,
            make_chunks
        )
        
        print(f"ZIM path: {ZIM_PATH}")
        print(f"Article title: {ARTICLE_TITLE}")
        print(f"Max chars: {MAX_CHARS}")
        
        # Test that ZIM file exists
        if not ZIM_PATH.exists():
            print(f"ERROR: ZIM file not found at {ZIM_PATH}")
            return False
            
        # Test the chunking process
        from libzim.reader import Archive
        from bs4 import BeautifulSoup
        
        archive = Archive(ZIM_PATH)
        html_content = article_html(archive, ARTICLE_TITLE)
        
        soup = BeautifulSoup(html_content, "lxml")
        content = soup.select_one(".mw-parser-output")
        
        if content is None:
            print("ERROR: Could not find .mw-parser-output in the article.")
            return False
            
        # Test the chunking process
        records = eligible_records(content)
        chunks = make_chunks(records, MAX_CHARS)
        
        print(f"SUCCESS: Processed {len(records)} records into {len(chunks)} chunks")
        
        if chunks:
            print(f"First chunk (section: {chunks[0]['section']}, chars: {len(str(chunks[0]['text']))}):")
            print(chunks[0]['text'][:200] + "..." if len(str(chunks[0]['text'])) > 200 else chunks[0]['text'])
        
        return True
        
    except Exception as e:
        print(f"ERROR: Chunking test failed - {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the chunking test."""
    print("=" * 60)
    print("TESTING CHUNKING FUNCTIONALITY")
    print("=" * 60)
    
    success = test_chunking_functionality()
    
    print("=" * 60)
    if success:
        print("CHUNKING TEST PASSED")
        print("The chunking functionality is working correctly.")
    else:
        print("CHUNKING TEST FAILED")
        print("There are issues with the chunking process.")
        
    print("=" * 60)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())