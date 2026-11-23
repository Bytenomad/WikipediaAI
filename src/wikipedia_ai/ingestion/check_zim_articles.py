#!/usr/bin/env python3
"""
Check what articles are available in the Wikipedia ZIM file.
"""

from libzim.reader import Archive
from pathlib import Path

# Use the same path as defined in chunking.py
ZIM_PATH = Path(r"D:\WikipediaAI\wikipedia\downloads\wikipedia_en_all_maxi_2026-08.zim")

def list_articles():
    """List articles from the ZIM file."""
    if not ZIM_PATH.is_file():
        print(f"ZIM file not found: {ZIM_PATH}")
        return
    
    try:
        archive = Archive(ZIM_PATH)
        print("Successfully opened ZIM file")
        
        # Try to get a sample of entries with different filtering approaches
        print("First 20 entries (with path info):")
        count = 0
        for entry in archive:  # This is the correct way to iterate
            if count >= 20:
                break
            print(f"  Title: '{entry.title}' | Path: '{entry.path}'")
            count += 1
            
    except Exception as e:
        print(f"Error reading ZIM file: {e}")

if __name__ == "__main__":
    list_articles()