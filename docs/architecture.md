# Wikipedia AI System Architecture

## Overview

Wikipedia AI is a local system for processing and retrieving Wikipedia content using offline ZIM archives, local embeddings (Ollama), and vector storage (Qdrant). The system enables natural language queries against Wikipedia's vast knowledge base.

## Package Structure

```
src/wikipedia_ai/
├── ingestion/          # Core data pipeline components
│   ├── __init__.py
│   ├── article_ingestion.py    # Main article processing logic
│   ├── batch_embeddings.py     # Embedding generation from text batches  
│   ├── chunking.py             # HTML content parsing and paragraph splitting
│   ├── qdrant_batch.py         # Qdrant vector storage operations
│   ├── progress_tracking.py    # SQLite-based progress tracking
│   ├── config.py               # Configuration fingerprinting
│   ├── enumeration.py          # Article enumeration from ZIM archives
│   └── cleanup.py              # Vector cleanup operations
├── storage/            # Database and Qdrant handling  
│   ├── __init__.py
│   ├── qdrant_client.py
│   └── sqlite_db.py
└── utils/              # Utility functions and helpers
    └── __init__.py
```

## Key Components

### 1. Ingestion Pipeline
The system follows a structured pipeline:
- Article enumeration from ZIM archive
- HTML parsing and content filtering  
- Paragraph chunking with section metadata
- Text embedding generation using local Ollama model
- Vector storage in Qdrant with deterministic point IDs
- Progress tracking through SQLite database

### 2. Configuration and Checkpointing
- Configuration fingerprinting based on source code hashes to ensure reproducibility
- Checkpoint management for resumable ingestion
- Deterministic Qdrant point ID generation

### 3. Safety Mechanisms
- Legacy ingestion disabled by default to prevent accidental data corruption
- Configuration identity verification to maintain checkpoint consistency  
- Isolated progress tracking with SQLite
- Collection validation prevents writes to wrong collections

## Data Flow

```
ZIM Archive  →  Article Enumeration  →  Content Parsing  →  Chunking  →  
Embedding Generation  →  Qdrant Storage  →  Query Interface
    ↑                           ↓
SQLite Progress Tracking   ←
```

## Dependencies

- Python 3.13+
- libzim for reading ZIM archives
- Ollama for local embeddings 
- Qdrant for vector database storage