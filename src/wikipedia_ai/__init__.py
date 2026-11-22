"""
Wikipedia AI - Local retrieval system with LLM integration.

A structured Python project for processing Wikipedia content using offline 
ZIM archives, local embeddings (Ollama), and vector storage (Qdrant).
"""
__version__ = "0.1.0"
__author__ = "AI Development Team"

# Import key components at package level
from .ingestion import *