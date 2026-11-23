"""
Image extraction functionality for Wikipedia articles.
This module extracts image URLs and metadata from Wikipedia HTML content.
"""

import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests
import os
import hashlib
from pathlib import Path

# Local directory to store downloaded images
LOCAL_IMAGE_DIR = "./open-webui/uploads/images"

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
            
            # Create image data structure with local storage info
            image_data = {
                'url': full_url,
                'alt_text': alt_text,
                'width': width,
                'height': height,
                'caption': caption,
                'source_tag': str(img_tag),
                'local_path': None  # Will be set when downloaded
            }
            
            images.append(image_data)
    
    return images

def download_and_save_image(image_url, local_dir=LOCAL_IMAGE_DIR):
    """
    Download an image from URL and save it locally.
    
    Args:
        image_url (str): URL of the image to download
        local_dir (str): Directory to save the image
        
    Returns:
        str: Local file path of downloaded image, or None if failed
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(local_dir, exist_ok=True)
        
        # Generate a unique filename based on URL hash
        url_hash = hashlib.md5(image_url.encode()).hexdigest()
        filename = f"{url_hash}.jpg"  # Default to jpg format
        
        # Determine file extension from URL or content
        parsed_url = urlparse(image_url)
        if parsed_url.path:
            ext = os.path.splitext(parsed_url.path)[1].lower()
            if ext and ext != '.jpg':
                filename = f"{url_hash}{ext}"
        
        local_path = os.path.join(local_dir, filename)
        
        # Only download if file doesn't exist
        if not os.path.exists(local_path):
            print(f"Downloading image: {image_url}")
            
            # Add headers to mimic a browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(image_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Saved image to: {local_path}")
        
        return local_path
    
    except Exception as e:
        print(f"Error downloading image {image_url}: {e}")
        return None

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
                    'source_tag': str(img_tag),
                    'local_path': None  # Will be set when downloaded
                }
                images.append(image_data)
    
    return images

def save_images_locally(images):
    """
    Download and save all images to local storage.
    
    Args:
        images (list): List of image dictionaries
        
    Returns:
        list: Updated list of image dictionaries with local paths
    """
    updated_images = []
    
    for img in images:
        # Download the image if not already saved
        if img.get('url'):
            local_path = download_and_save_image(img['url'])
            img['local_path'] = local_path
        updated_images.append(img)
    
    return updated_images

# Example usage
if __name__ == "__main__":
    # This would be used in your main processing pipeline
    print("Image extraction module loaded successfully")