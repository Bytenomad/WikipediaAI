# Wikipedia AI

A local system for processing and retrieving Wikipedia content using offline ZIM archives, local embeddings (Ollama), and vector storage (Qdrant).

## Overview

This project enables natural language queries against Wikipedia's vast knowledge base using local processing. It processes articles from an offline Wikipedia ZIM archive, generates embeddings locally using Ollama, stores vectors in Qdrant for efficient retrieval, and maintains a robust progress tracking system.

## Features

- Offline Wikipedia processing (using ZIM archives)  
- Local embedding generation with Ollama
- Vector storage in Qdrant with deterministic point IDs
- Progress tracking and resumable ingestion
- Safety mechanisms to prevent data corruption
- Configuration fingerprinting for consistent processing

## Architecture

```
ZIM Archive  →  Article Enumeration  →  Content Parsing  →  Chunking  →  
Embedding Generation  →  Qdrant Storage  →  Query Interface
    ↑                           ↓
SQLite Progress Tracking   ←
```

## Prerequisites

- Python 3.13+
- Ollama installed and running local embedding model
- Qdrant server running locally
- Wikipedia ZIM archive (`wikipedia/downloads/wikipedia_en_all_maxi_2026-08.zim`)

## Setup

### Development Environment

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd WikipediaAI
   ```

2. Install requirements:
   ```bash
   pip install -e .
   ```

3. Run tests to verify setup:
   ```bash
   pytest
   ```

## Project Structure

```
C:\WikipediaAI\
├── src\wikipedia_ai\          # Main Python package
├── tests\                     # Test suite  
├── docs\                      # Documentation
├── wikipedia\                 # Runtime data (ZIM archives, etc.)
└── pyproject.toml             # Package configuration
```

## Safety Protocols

The system includes multiple safety mechanisms:
- Legacy ingestion is disabled by default 
- Configuration fingerprinting ensures consistent processing
- Progress tracking prevents duplicate processing  
- Collection validation prevents wrong storage targets

## Documentation

- [Architecture](docs/architecture.md)
- [Development Setup](docs/development.md) 
- [Ingestion Lifecycle](docs/ingestion-lifecycle.md)
- [Safety Protocols](docs/safety.md)

## Contributing

This project follows standard Python packaging practices with unit and integration tests. All contributions must:
1. Pass existing tests
2. Maintain configuration identity compatibility
3. Not affect production data during development  

## License

MIT