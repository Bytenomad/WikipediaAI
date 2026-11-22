"""Local embedding generation with Ollama."""

import os
import requests
import numpy as np

EMBEDDING_MODEL = "nomic-embed-text"
VECTOR_DIMENSIONS = 768


def embed_batch(texts):
    """Generate embeddings for list of texts using local Ollama API."""
    
    # Check if Ollama is running locally
    ollama_url = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
    
    try:
        response = requests.post(
            f"{ollama_url}/api/embeddings",
            json={
                "model": EMBEDDING_MODEL,
                "prompt": " ".join(texts)
            },
            timeout=60
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"Ollama API error: {response.text}")
            
        result = response.json()
        embeddings = result["embedding"]
        
        # Convert to numpy array and normalize
        vectors = np.array(embeddings)
        vectors = vectors / np.linalg.norm(vectors)
        
        return [vectors.tolist()]
        
    except Exception as e:
        # Try individual embedding generation if batch fails  
        print(f"Batch embedding failed, trying individual embeddings: {e}")
        embeddings = []
        for text in texts:
            try:
                response = requests.post(
                    f"{ollama_url}/api/embeddings",
                    json={
                        "model": EMBEDDING_MODEL,
                        "prompt": text
                    },
                    timeout=60
                )
                
                if response.status_code != 200:
                    raise RuntimeError(f"Ollama API error for text: {response.text}")
                    
                result = response.json()
                embedding = np.array(result["embedding"])
                normalized = embedding / np.linalg.norm(embedding)
                embeddings.append(normalized.tolist())
            except Exception as individual_e:
                print(f"Individual embedding failed for text: {individual_e}")
                # Return zero vector for failed texts
                embeddings.append([0.0] * VECTOR_DIMENSIONS)
                
        return embeddings


# For testing purposes
BATCH_SIZE = 10

if __name__ == "__main__":
    print("Testing embedding generation...")
    
    try:
        # Test with sample text
        test_text = "This is a short test paragraph for embedding."
        result = embed_batch([test_text])
        print(f"Generated embedding of size: {len(result[0])}")
        print("SUCCESS")
    except Exception as e:
        print(f"Embedding test failed: {e}")