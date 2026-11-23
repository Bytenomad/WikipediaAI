#!/usr/bin/env python3
"""
Test script to verify we can extract content from the ZIM file properly.
"""

from libzim.reader import Archive
from pathlib import Path
from bs4 import BeautifulSoup
import sys

# Use the same path as defined in chunking.py
ZIM_PATH = Path(r"D:\WikipediaAI\wikipedia\downloads\wikipedia_en_all_maxi_2026-08.zim")
ARTICLE_TITLE = "Medicine"

def extract_article_content():
    """Extract content from a Wikipedia article in the ZIM file."""
    if not ZIM_PATH.is_file():
        print(f"ZIM file not found: {ZIM_PATH}")
        return None
    
    try:
        archive = Archive(ZIM_PATH)
        print("Successfully opened ZIM file")
        
        # Try to find the article
        entry = None
        for item in archive:
            if item.title == ARTICLE_TITLE:
                entry = item
                break
                
        if entry is None:
            print(f"Article '{ARTICLE_TITLE}' not found in ZIM file")
            return None
            
        print(f"Found article: {entry.title}")
        
        # Get the content of the article
        item = entry.get_item()
        content = bytes(item.content).decode("UTF-8")
        
        print(f"Content length: {len(content)} characters")
        print("First 500 characters:")
        print(content[:500])
        
        # Try to parse with BeautifulSoup
        soup = BeautifulSoup(content, "html.parser")
        print("\nParsed content - title:", soup.title.text if soup.title else "No title")
        
        # Look for main content area (mw-parser-output)
        parser_output = soup.find("div", {"class": "mw-parser-output"})
        if parser_output:
            print("Found mw-parser-output div")
            # Get first few paragraphs
            paragraphs = parser_output.find_all("p")[:3]
            for i, p in enumerate(paragraphs):
                print(f"Paragraph {i+1}: {p.get_text()[:200]}...")
        else:
            print("No mw-parser-output found")
            
        return content
        
    except Exception as e:
        print(f"Error reading ZIM file: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    extract_article_content()