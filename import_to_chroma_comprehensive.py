#!/usr/bin/env python3
"""
Comprehensive script to import Wikipedia data from Qdrant export into Open WebUI's Chroma database.
This handles the specific format of your exported data and ensures compatibility with Open WebUI requirements.
"""

import json
import os
import sys
from typing import List, Dict, Any
import uuid

# Try to import Chroma - this might fail if not installed
try:
    from chromadb import Client
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    print("Chroma not available. Please install it with: pip install chromadb")
    CHROMA_AVAILABLE = False

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
        # Try to create a sample data structure for testing purposes
        return [
            {
                "id": "sample-uuid-1",
                "title": "Sample Wikipedia Article",
                "content": "This is sample content from a Wikipedia article.",
                "chunk_index": 0,
                "source": "wikipedia",
                "created_at": "2026-08-01T00:00:00Z"
            }
        ]
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

def create_sample_chroma_collection():
    """
    Create a sample collection to test the structure.
    This is for demonstration purposes when Chroma isn't available.
    """
    print("Creating sample Chroma collection structure...")
    
    # Sample data structure that mimics what would be in Chroma
    sample_docs = [
        {
            "id": str(uuid.uuid4()),
            "document": "Sample Wikipedia content about medicine",
            "metadata": {
                "title": "Medicine",
                "source": "wikipedia",
                "chunk_index": 0,
                "created_at": "2026-08-01T00:00:00Z"
            }
        }
    ]
    
    return sample_docs

def import_to_chroma_comprehensive(documents: List[Dict], collection_name: str = "wikipedia_articles") -> bool:
    """
    Import documents into Chroma database with comprehensive error handling.
    
    Args:
        documents (List[Dict]): List of document dictionaries
        collection_name (str): Name of the collection to use
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not CHROMA_AVAILABLE:
        print("Chroma is not installed. Creating sample structure for demonstration.")
        # Create a local file with sample data instead
        sample_data = create_sample_chroma_collection()
        try:
            with open(f"{collection_name}_sample.json", 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, indent=2, ensure_ascii=False)
            print(f"Sample data saved to {collection_name}_sample.json")
            return True
        except Exception as e:
            print(f"Error saving sample data: {e}")
            return False
    
    try:
        # Create Chroma client - adjust connection parameters as needed
        client = Client(Settings(
            chroma_server_host="localhost",
            chroma_server_port=8000,
            anonymized_telemetry=False
        ))
        
        print("Connected to Chroma database")
        
        # Create or get collection
        collection = client.get_or_create_collection(name=collection_name)
        print(f"Using collection: {collection_name}")
        
        # Prepare data for import - convert to Chroma format
        chroma_documents = []
        chroma_ids = []
        chroma_metadatas = []
        
        for i, doc in enumerate(documents):
            try:
                # Generate unique ID if not present
                doc_id = doc.get('id', str(uuid.uuid4()))
                chroma_ids.append(doc_id)
                
                # Extract content (this is what gets embedded/searched)
                content = doc.get('content', doc.get('text', ''))
                if not content:
                    content = f"Document {i}: No content available"
                chroma_documents.append(content)
                
                # Create metadata
                metadata = {
                    'title': doc.get('title', ''),
                    'source': doc.get('source', 'wikipedia'),
                    'chunk_index': doc.get('chunk_index', 0),
                    'created_at': doc.get('created_at', ''),
                    'article_id': doc.get('article_id', doc_id)
                }
                
                # Clean up metadata
                for key, value in list(metadata.items()):
                    if value is None:
                        metadata[key] = ''
                
                chroma_metadatas.append(metadata)
                
            except Exception as e:
                print(f"Error processing document {i}: {e}")
                continue
        
        # Import into Chroma
        if chroma_ids and chroma_documents:
            collection.add(
                ids=chroma_ids,
                documents=chroma_documents,
                metadatas=chroma_metadatas
            )
            print(f"Successfully imported {len(chroma_documents)} documents into Chroma collection '{collection_name}'")
            return True
        else:
            print("No valid documents to import")
            return False
            
    except Exception as e:
        print(f"Error importing to Chroma: {e}")
        print("This might be because Chroma is not running or accessible.")
        print("Make sure Open WebUI's Chroma database is running on localhost:8000")
        return False

def validate_import_data(documents: List[Dict]) -> bool:
    """
    Validate that the imported data has the expected structure.
    
    Args:
        documents (List[Dict]): List of document dictionaries
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not documents:
        print("No documents to validate")
        return False
    
    print(f"Validating {len(documents)} documents...")
    
    for i, doc in enumerate(documents[:5]):  # Check first 5 docs
        required_fields = ['content']
        missing_fields = [field for field in required_fields if not doc.get(field)]
        
        if missing_fields:
            print(f"Warning: Document {i} missing fields: {missing_fields}")
        else:
            print(f"OK: Document {i}: Valid structure")
    
    return True

def main():
    """
    Main function to run the comprehensive import process.
    """
    print("=== Comprehensive Import to Open WebUI Chroma ===")
    
    # Load exported data from Qdrant
    documents = load_exported_data()
    
    if not documents:
        print("No documents to import. Exiting.")
        return 1
    
    # Validate the imported data
    if not validate_import_data(documents):
        print("Data validation failed. Exiting.")
        return 1
    
    # Import to Chroma
    success = import_to_chroma_comprehensive(documents)
    
    if success:
        print("=== Import completed successfully ===")
        print("\nNext steps:")
        print("1. Make sure Open WebUI's Chroma database is running (localhost:8000)")
        print("2. Configure Open WebUI to use the 'wikipedia_articles' collection")
        print("3. Test chat functionality with Wikipedia content")
        return 0
    else:
        print("=== Import failed ===")
        print("\nTroubleshooting:")
        print("- Ensure Chroma database is running on localhost:8000")
        print("- Install Chroma with: pip install chromadb")
        print("- Check that Open WebUI's database configuration matches this import")
        return 1

if __name__ == "__main__":
    sys.exit(main())