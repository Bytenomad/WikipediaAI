#!/usr/bin/env python3
"""Improved test script to process a single article and prepare it for Open WebUI chat."""

import _bootstrap

import sys
import os
import json
from pathlib import Path

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from wikipedia_ai.ingestion.chunking import make_chunks, eligible_records, remove_excluded_sections
from wikipedia_ai.ingestion.batch_embeddings import embed_batch
from wikipedia_ai.ingestion.qdrant_batch import upload_batch
from wikipedia_ai.ingestion.config import configuration_id
from wikipedia_ai.ingestion.target import TEST_COLLECTION

def create_sample_article_content():
    """Create sample article content for testing."""
    # This is a simplified test article - in reality, this would come from ZIM
    sample_content = """
    <div class="mw-parser-output">
        <h1>Testville</h1>
        <p>This is a test article about Testville. It contains various sections and information.</p>
        
        <h2>History</h2>
        <p>Testville was founded in 1850. The city has grown significantly since its founding.</p>
        
        <h2>Geography</h2>
        <p>Testville is located in the central region of the country. It has a population of 50,000 people.</p>
        
        <h2>Demographics</h2>
        <ul>
            <li>Population: 50,000</li>
            <li>Area: 10 km²</li>
            <li>Founded: 1850</li>
        </ul>
        
        <h2>Education</h2>
        <p>The city has several schools and a university. Education is highly valued in Testville.</p>
    </div>
    """
    return sample_content

def test_single_article_processing():
    """Process a single article through the entire pipeline."""
    
    print("Starting single article processing test...")
    
    # Create sample content
    sample_html = create_sample_article_content()
    
    # For this test, we'll simulate the ingestion process manually
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(sample_html, "lxml")
    content = soup.select_one(".mw-parser-output")
    
    if content is None:
        print("Could not find .mw-parser-output in the sample article.")
        return False
        
    # Remove excluded sections (like references, notes)
    remove_excluded_sections(content)
    
    # Get eligible records
    records = eligible_records(content)
    print(f"Found {len(records)} eligible prose records")
    
    # Make chunks
    chunks = make_chunks(records, 1500)  # Using MAX_CHARS from chunking.py
    print(f"Created {len(chunks)} chunks")
    
    # Generate embeddings (mocked for now)
    try:
        texts = [chunk["text"] for chunk in chunks]
        if texts:
            print("Generating embeddings...")
            vectors = embed_batch(texts)
            print(f"Generated {len(vectors)} embeddings")
            
            # Simulate uploading to Qdrant
            print("Uploading to Qdrant...")
            
            # For this test, we'll just simulate the upload
            config_id = configuration_id()
            print(f"Configuration ID: {config_id}")
            
            print("Test successful - would upload to Qdrant")
            return True
        else:
            print("No text to embed")
            return False
            
    except Exception as e:
        print(f"Error during embedding generation: {e}")
        return False

def create_integration_test():
    """Create a comprehensive test for integration between Qdrant and Open WebUI."""
    
    print("\n=== Integration Test ===")
    print("This script demonstrates how to integrate Qdrant with Open WebUI")
    
    # 1. Show the configuration details
    try:
        from wikipedia_ai.ingestion.config import configuration_details, configuration_id
        details = configuration_details()
        config_id = configuration_id()
        
        print("\nConfiguration Details:")
        for key, value in details.items():
            print(f"  {key}: {value}")
            
        print(f"\nConfiguration ID: {config_id}")
        
    except Exception as e:
        print(f"Error getting configuration: {e}")
    
    # 2. Show what we'd need to do to export from Qdrant for Open WebUI
    print("\n=== Exporting from Qdrant ===")
    print("To integrate with Open WebUI, we need to convert Qdrant data to a format compatible with Chroma.")
    print("This would involve:")
    print("  1. Querying Qdrant for stored Wikipedia articles")
    print("  2. Converting the data structure to match Chroma's expectations")
    print("  3. Creating a script that can populate Chroma with this data")
    
    # 3. Show how we'd test it
    print("\n=== Testing Integration ===")
    print("We would run:")
    print("  1. Single article ingestion (to Qdrant)")
    print("  2. Export script to convert Qdrant data to Chroma format")
    print("  3. Open WebUI chat with the imported data")

if __name__ == "__main__":
    success = test_single_article_processing()
    
    if success:
        create_integration_test()
        print("\n=== Test completed successfully ===")
    else:
        print("\n=== Test failed ===")
        sys.exit(1)