"""
Response formatter for Wikipedia AI integration.
This module handles formatting of responses that include local image references
for proper display in Open WebUI chat interface.
"""

import re
from typing import List, Dict, Any

def format_response_with_images(response_text: str, images: List[Dict[str, Any]] = None) -> str:
    """
    Format a response text to include proper image references for Open WebUI display.
    
    Args:
        response_text (str): The original response text from the LLM
        images (List[Dict]): List of image information including local paths
        
    Returns:
        str: Formatted response with image markdown references
    """
    if not images or not isinstance(images, list):
        return response_text
    
    # Create a copy of the response text to modify
    formatted_response = response_text
    
    # Process each image and add appropriate markdown references
    for i, image in enumerate(images):
        # Check if we have local path information
        if 'local_path' in image and image['local_path']:
            local_path = image['local_path']
            
            # Extract just the filename from the full path
            filename = local_path.split('/')[-1]  # Unix-style path
            
            # Create markdown image reference
            # Open WebUI should be able to display images when they're accessible via relative paths
            image_markdown = f"![Image {i+1}]({filename})"
            
            # Add the image reference to the response text (at the end for now)
            # In a real implementation, you might want to place it near relevant content
            if formatted_response:
                formatted_response += f"\n\n{image_markdown}"
            else:
                formatted_response = image_markdown
    
    return formatted_response


def format_rag_response_with_images(response_text: str, chunk_data: Dict[str, Any]) -> str:
    """
    Format a RAG response that includes images from the retrieved chunks.
    
    Args:
        response_text (str): The LLM-generated response text
        chunk_data (Dict): Data about the retrieved chunks including image information
        
    Returns:
        str: Formatted response with proper image references
    """
    if not chunk_data or 'images' not in chunk_data:
        return response_text
    
    images = chunk_data.get('images', [])
    
    # If we have images, format them into markdown
    formatted_response = response_text
    
    # Add all images at the end of the response
    if images and isinstance(images, list):
        image_references = []
        for i, img_path in enumerate(images):
            if isinstance(img_path, str) and img_path:
                filename = img_path.split('/')[-1]  # Extract filename from path
                image_references.append(f"![Image {i+1}]({filename})")
        
        if image_references:
            formatted_response += "\n\n" + "\n\n".join(image_references)
    
    return formatted_response


def create_image_markdown_references(images: List[str]) -> str:
    """
    Create markdown image references from a list of local image paths.
    
    Args:
        images (List[str]): List of local image file paths
        
    Returns:
        str: Markdown formatted image references
    """
    if not images or not isinstance(images, list):
        return ""
    
    markdown_refs = []
    for i, img_path in enumerate(images):
        if isinstance(img_path, str) and img_path:
            filename = img_path.split('/')[-1]  # Extract filename from path
            markdown_refs.append(f"![Image {i+1}]({filename})")
    
    return "\n\n".join(markdown_refs)


def process_chunk_with_images(chunk_text: str, chunk_images: List[Dict[str, Any]] = None) -> str:
    """
    Process a text chunk and add image references if available.
    
    Args:
        chunk_text (str): The text content of the chunk
        chunk_images (List[Dict]): List of image data for this chunk
        
    Returns:
        str: Chunk text with image references added
    """
    if not chunk_images or not isinstance(chunk_images, list):
        return chunk_text
    
    # Add image references to the chunk text
    image_refs = create_image_markdown_references([img.get('local_path') for img in chunk_images if 'local_path' in img and img['local_path']])
    
    if image_refs:
        return f"{chunk_text}\n\n{image_refs}"
    
    return chunk_text


# Example usage function
def example_usage():
    """Example of how to use the response formatter."""
    # Sample data
    sample_response = "This is a sample response about medicine. The information comes from Wikipedia articles."
    sample_images = [
        {"local_path": "./open-webui/uploads/images/abc123.jpg", "alt_text": "A medical illustration"},
        {"local_path": "./open-webui/uploads/images/def456.png", "alt_text": "A diagram of human anatomy"}
    ]
    
    # Format the response
    formatted = format_response_with_images(sample_response, sample_images)
    print(formatted)


if __name__ == "__main__":
    example_usage()