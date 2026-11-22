"""Generate embeddings for batches of Wikipedia text using local Ollama."""

import time
import requests

from pathlib import Path

# The embedding model to use (should be configurable)
EMBEDDING_MODEL = "nomic-embed-text"
VECTOR_DIMENSIONS = 768
BATCH_SIZE = 32


def embed_batch(texts):
    """Generate embeddings for a batch of texts."""
    
    # Make a call to local Ollama embedding API 
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": EMBEDDING_MODEL,
            "prompt": "\n\n".join(texts)
        }
    )
    
    if response.status_code != 200:
        raise RuntimeError(f"Ollama embedding API error: {response.text}")
        
    data = response.json()
    
    # Note: For multiple texts, Ollama returns a list of embeddings
    # This may need to be adjusted based on the exact Ollama API response format
    return [
        embedding for embedding in data['embeddings']
    ]


if __name__ == "__main__":
    print("Batch embeddings module test")
    print(f"Using model: {EMBEDDING_MODEL}")
    
    # Test with a simple example
    sample_text = "This is a test sentence for embedding."
    result = embed_batch([sample_text])
    
    if len(result) > 0:
        print(f"Generated {len(result)} embeddings")
        print(f"Vector dimension: {len(result[0])}")
        print("SUCCESS: Embedding generation works")
    else:
        print("ERROR: No embeddings generated")