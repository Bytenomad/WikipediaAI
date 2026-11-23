"""
Response formatter for Wikipedia AI integration.
This module ensures that images are properly formatted for display in Open WebUI chat interface.
"""

import os
from typing import Dict, List, Any

# Local directory where images are stored (should match the one used in image_extraction.py)
LOCAL_IMAGE_DIR = "./open-webui/uploads/images"

def format_response_with_images(content: str, images: List[str] = None) -> str:
    """
    Format content to include proper image references for Open WebUI.
    
    Args:
        content (str): The text content to format
        images (List[str]): List of local image paths to include
        
    Returns:
        str: Formatted content with image references
    """
    if not images:
        return content
    
    # Create image markdown references for Open WebUI
    image_references = []
    
    for img_path in images:
        if img_path:
            # Get just the filename for display
            filename = os.path.basename(img_path)
            
            # Create a relative path that Open WebUI can access
            # This assumes the image directory is mounted at /app/uploads/images in Open WebUI container
            relative_path = f"uploads/images/{filename}"
            
            # Add image reference in markdown format
            image_references.append(f"![Image]({relative_path})")
    
    if image_references:
        # Append images to the content
        formatted_content = content + "\n\n" + "\n".join(image_references)
        return formatted_content
    
    return content

def process_qdrant_payload_for_chat(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process Qdrant payload to prepare it for chat response formatting.
    
    Args:
        payload (Dict): The raw Qdrant payload from database
        
    Returns:
        Dict: Processed payload with proper image references
    """
    # Extract images from the payload if they exist
    images = payload.get('images', [])
    
    # If we have image paths, format them properly for Open WebUI display
    if images and isinstance(images, list):
        # Ensure we're working with local paths that can be converted to web-accessible URLs
        formatted_images = []
        
        for img in images:
            if isinstance(img, str) and os.path.exists(img):
                formatted_images.append(img)
            elif isinstance(img, dict) and 'local_path' in img:
                formatted_images.append(img['local_path'])
                
        # Store the formatted images in a way that Open WebUI can understand
        payload['formatted_images'] = formatted_images
    
    return payload

def create_chat_response(content: str, metadata: Dict[str, Any] = None) -> str:
    """
    Create a properly formatted chat response with images.
    
    Args:
        content (str): The main content text
        metadata (Dict): Metadata including image information
        
    Returns:
        str: Formatted response ready for Open WebUI chat
    """
    # Extract images from metadata if they exist
    images = None
    if metadata and 'images' in metadata:
        images = metadata['images']
    
    # Format the content with image references
    return format_response_with_images(content, images)

def create_chat_response_with_local_paths(content: str, local_image_paths: List[str] = None) -> str:
    """
    Create a chat response with properly formatted local image paths for Open WebUI.
    
    Args:
        content (str): The main content text
        local_image_paths (List[str]): List of local image file paths
        
    Returns:
        str: Formatted response ready for Open WebUI chat with local images
    """
    if not local_image_paths:
        return content
    
    # Create relative paths that Open WebUI can access
    image_references = []
    for img_path in local_image_paths:
        if img_path:
            filename = os.path.basename(img_path)
            # This assumes the Docker volume is mounted at /app/uploads/images
            relative_path = f"uploads/images/{filename}"
            image_references.append(f"![Image]({relative_path})")
    
    if image_references:
        formatted_content = content + "\n\n" + "\n".join(image_references)
        return formatted_content
    
    return content