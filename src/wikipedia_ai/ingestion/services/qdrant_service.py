"""
Abstract base class for Qdrant services.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


class QdrantServiceError(Exception):
    """Custom exception for Qdrant service errors."""
    pass


@dataclass
class VectorRecord:
    """Data class representing a vector record in Qdrant."""
    id: str
    vector: List[float]
    metadata: Dict[str, Any]
    payload: Dict[str, Any]


class QdrantService(ABC):
    """Abstract base class for Qdrant vector storage services."""

    @abstractmethod
    def initialize_collection(self, collection_name: str, 
                            vector_size: int, 
                            distance: str = "Cosine") -> None:
        """
        Initialize a collection with the specified parameters.

        Args:
            collection_name: Name of the collection to create
            vector_size: Size of vectors in the collection
            distance: Distance metric to use (default: "Cosine")
        """
        pass

    @abstractmethod
    def upload_batch(self, 
                    collection_name: str,
                    records: List[VectorRecord]) -> None:
        """
        Upload a batch of records to Qdrant.

        Args:
            collection_name: Name of the collection to upload to
            records: List of VectorRecord objects to upload
        """
        pass

    @abstractmethod
    def search(self, 
              collection_name: str,
              vector: List[float],
              limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in the collection.

        Args:
            collection_name: Name of the collection to search
            vector: Query vector to search for
            limit: Maximum number of results to return

        Returns:
            List of search results with metadata
        """
        pass


class QdrantServiceError(Exception):
    """Custom exception for Qdrant service errors."""
    pass