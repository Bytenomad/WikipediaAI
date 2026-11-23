#!/usr/bin/env python3
"""
Script to import Wikipedia data from Qdrant export into Open WebUI's Chroma database.
This converts the exported JSON format into a format compatible with Chroma.
"""

import json
import os
import sys
from typing import List, Dict, Any
from chromadb import Client
from chromadb.config import Settings

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(__file__))

def load_exported_data(file_path: str = "qdrant_export.json") -> List[Dict]:
    """
    Load the exported data from Qdrant.
    
    Args:
        file_path (str): Path to the exported JSON file
        
    Returns:
        List[Dict]: List of document dictionaries
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Loaded {len(data)} documents from {file_path}")
        return data
    except FileNotFoundError:
        print(f"Error: Export file {file_path} not found")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

def create_chroma_client() -> Client:
    """
    Create a Chroma client.
    
    Returns:
        Client: Chroma client instance
    """
    try:
        # Default Chroma settings - adjust as needed for your Open WebUI setup
        client = Client(Settings(
            chroma_api_add_header="Authorization: Bearer your-api-key-here",  # Replace with actual key if needed
            chroma_server_host="localhost",
            chroma_server_port=8000,
            anonymized_telemetry=False
        ))
        print("Successfully connected to Chroma database")
        return client
    except Exception as e:
        print(f"Failed to connect to Chroma: {e}")
        # Try connection without auth header for local setup
        try:
            client = Client(Settings(
                chroma_server_host="localhost",
                chroma_server_port=8000,
                anonymized_telemetry=False
            ))
            print("Successfully connected to Chroma database (no auth)")
            return client
        except Exception as e2:
            print(f"Failed to connect to Chroma even without auth: {e2}")
            return None

def import_to_chroma(documents: List[Dict], collection_name: str = "wikipedia_articles") -> bool:
    """
    Import documents into Chroma database.
    
    Args:
        documents (List[Dict]): List of document dictionaries
        collection_name (str): Name of the collection to use
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create or get client
        client = create_chroma_client()
        if not client:
            return False
            
        # Create or get collection
        collection = client.get_or_create_collection(name=collection_name)
        print(f"Using collection: {collection_name}")
        
        # Prepare data for Chroma import
        ids = []
        contents = []
        metadatas = []
        
        for i, doc in enumerate(documents):
            # Generate unique ID if not present
            doc_id = doc.get('id', f'doc_{i}')
            ids.append(doc_id)
            
            # Use content field as the main text
            content = doc.get('content', '')
            contents.append(content)
            
            # Create metadata dictionary
            metadata = {
                'title': doc.get('title', ''),
                'source': doc.get('source', 'wikipedia'),
                'chunk_index': doc.get('chunk_index', 0),
                'created_at': doc.get('created_at', ''),
                'article_id': doc.get('article_id', '')
            }
            metadatas.append(metadata)
            
        # Import into Chroma
        if ids and contents:
            collection.add(
                ids=ids,
                documents=contents,
                metadatas=metadatas
            )
            print(f"Successfully imported {len(documents)} documents into Chroma collection '{collection_name}'")
            return True
        else:
            print("No documents to import")
            return False
            
    except Exception as e:
        print(f"Error importing to Chroma: {e}")
        return False

def main():
    """
    Main function to run the import process.
    """
    print("=== Importing Wikipedia Data to Open WebUI Chroma ===")
    
    # Load exported data from Qdrant
    documents = load_exported_data()
    
    if not documents:
        print("No documents to import. Exiting.")
        return 1
    
    # Import to Chroma
    success = import_to_chroma(documents)
    
    if success:
        print("=== Import completed successfully ===")
        return 0
    else:
        print("=== Import failed ===")
        return 1

if __name__ == "__main__":
    sys.exit(main())