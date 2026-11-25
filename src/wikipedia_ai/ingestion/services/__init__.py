"""
Services package for Wikipedia AI ingestion system.

This package provides abstract service definitions and implementations
for core functionality like embedding generation and vector storage.
"""

from .embedding_service import EmbeddingService, OllamaEmbeddingService
from .qdrant_service import QdrantService, QdrantServiceError

__all__ = [
    'EmbeddingService',
    'OllamaEmbeddingService',
    'QdrantService',
    'QdrantServiceError'
]