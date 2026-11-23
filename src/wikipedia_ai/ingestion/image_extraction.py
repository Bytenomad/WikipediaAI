"""
Image extraction functionality for Wikipedia articles.
This module extracts image URLs and metadata from Wikipedia HTML content.
"""

import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests

def extract_images_from_article(html_content, base_url=None):
    """
    Extract image information from Wikipedia article HTML
    
    Args:
        html_content (str): HTML content of the Wikipedia article
        base_url (str): Base URL for resolving relative URLs
        
    Returns:
        list: List of dictionaries containing image information
    """
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Find all images in the article
    images = []
    
    # Look for images in the main content area
    content_area = soup.select_one('.mw-parser-output')
    
    if content_area:
        # Find all img tags with src attributes
        img_tags = content_area.find_all('img', src=True)
        
        for img_tag in img_tags:
            # Extract image source
            src = img_tag.get('src', '')
            
            # Handle relative URLs
            if base_url and src.startswith('/'):
                full_url = urljoin(base_url, src)
            elif src.startswith('//'):
                full_url = 'https:' + src
            elif src.startswith('http'):
                full_url = src
            else:
                full_url = urljoin(base_url or 'https://en.wikipedia.org', src) if base_url else src
            
            # Extract alt text
            alt_text = img_tag.get('alt', '')
            
            # Extract width and height if available
            width = img_tag.get('width')
            height = img_tag.get('height')
            
            # Get image caption if available (look for surrounding elements)
            caption = ""
            parent = img_tag.parent
            
            # Look for captions in figure or div tags
            if parent:
                caption_element = parent.find('span', class_='image-caption') or \
                                parent.find('div', class_='thumbcaption') or \
                                parent.find('figcaption')
                
                if caption_element:
                    caption = caption_element.get_text(strip=True)
            
            # Create image data structure
            image_data = {
                'url': full_url,
                'alt_text': alt_text,
                'width': width,
                'height': height,
                'caption': caption,
                'source_tag': str(img_tag)
            }
            
            images.append(image_data)
    
    return images

def get_wikipedia_image_info(image_url):
    """
    Get additional information about a Wikipedia image
    
    Args:
        image_url (str): URL of the Wikipedia image
        
    Returns:
        dict: Image metadata
    """
    # This would be extended to fetch actual image metadata from Wikimedia
    # For now, we return basic info extracted from the HTML
    return {
        'url': image_url,
        'type': 'wikipedia',
        'is_available': True
    }

def extract_images_from_content(content_element):
    """
    Extract images from a BeautifulSoup content element
    
    Args:
        content_element: BeautifulSoup element containing article content
        
    Returns:
        list: List of image dictionaries
    """
    images = []
    
    # Look for images in various potential locations
    img_selectors = [
        '.mw-parser-output img',
        '.image img',
        '.thumb img',
        'figure img'
    ]
    
    for selector in img_selectors:
        img_tags = content_element.select(selector)
        for img_tag in img_tags:
            src = img_tag.get('src', '')
            alt_text = img_tag.get('alt', '')
            
            if src:
                image_data = {
                    'url': src,
                    'alt_text': alt_text,
                    'source_tag': str(img_tag)
                }
                images.append(image_data)
    
    return images

# Example usage
if __name__ == "__main__":
    # This would be used in your main processing pipeline
    print("Image extraction module loaded successfully")