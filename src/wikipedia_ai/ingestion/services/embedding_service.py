"""
Abstract base class for embedding services.
"""

from abc import ABC, abstractmethod
from typing import List, Union


class EmbeddingService(ABC):
    """Abstract base class for embedding generation services."""

    @abstractmethod
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors (each vector is a list of floats)

        Raises:
            Exception: If embedding generation fails
        """
        pass


class OllamaEmbeddingService(EmbeddingService):
    """Concrete implementation using Ollama for embedding generation."""

    def __init__(self, model_name: str = "nomic-embed-text", base_url: str = "http://localhost:11434"):
        """
        Initialize the Ollama embedding service.

        Args:
            model_name: Name of the embedding model to use
            base_url: Base URL for the Ollama API
        """
        self.model_name = model_name
        self.base_url = base_url

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using Ollama's API.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        import requests
        import json
        
        embeddings = []
        
        for text in texts:
            try:
                # Make a call to local Ollama embedding API 
                response = requests.post(
                    f"{self.base_url}/api/embeddings",
                    json={
                        "model": self.model_name,
                        "prompt": text
                    }
                )
                
                if response.status_code != 200:
                    raise RuntimeError(f"Ollama embedding API error: {response.text}")
                    
                data = response.json()
                
                # Handle Ollama API response correctly
                if 'embedding' in data:
                    # Single embedding returned in 'embedding' key  
                    embeddings.append(data['embedding'])
                else:
                    raise ValueError(f"Unexpected Ollama API response format: {json.dumps(data, indent=2)}")
                    
            except Exception as e:
                raise RuntimeError(f"Error generating embedding for text '{text[:50]}...': {e}")
        
        return embeddings