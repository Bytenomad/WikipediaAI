# Wikipedia AI Usage Guide

## Overview

This guide explains how to use the generation-aware Wikipedia AI ingestion pipeline that has been implemented. The system processes Wikipedia content locally for offline knowledge access.

## System Requirements

Before using the pipeline, ensure you have:

1. **Python 3.13+** installed
2. **Ollama** running locally with the `nomic-embed-text` model
3. **Qdrant server** running locally 
4. **Wikipedia ZIM archive** (e.g., `wikipedia_en_all_maxi_2026-08.zim`)
5. **Required Python packages** installed via: `pip install -e .`

## Quick Start

1. **Start Ollama and Qdrant services**:
   ```bash
   # Start Ollama (ensure nomic-embed-text is pulled)
   ollama pull nomic-embed-text
   
   # Start Qdrant (typically via Docker or local installation)  
   ```

2. **Install the package**:
   ```bash
   pip install -e .
   ```

3. **Run a single article ingestion**:
   ```bash
   python wikipedia/processing/ingestion/ingest_article.py "Article Title"
   ```

4. **Run pipeline verification tests**:
   ```bash 
   python wikipedia/processing/ingestion/final_verification.py
   ```

## Key Components

### 1. `ingest_article.py` - Main Entry Point
The core ingestion script that processes individual Wikipedia articles:

```bash
python ingest_article.py "Article Title"
```

### 2. `batch_embeddings.py` - Embedding Generation  
Generates vector embeddings using Ollama's local API.

### 3. `qdrant_batch.py` - Vector Storage 
Uploads embeddings to Qdrant with deterministic point IDs.

### 4. `article_generations.py` - Generation Management
Handles generation lifecycle: registration, validation, and publication.

### 5. `ingestion_progress.py` - Progress Tracking  
Tracks ingestion state in SQLite database.

## Architecture Features

### Generation Awareness
- Each ingestion run creates a unique generation ID 
- Only validated generations become visible to retrieval
- Prevents partial or failed ingestion from corrupting knowledge base

### Safety Mechanisms
- **Deterministic Point IDs**: UUID5-based point IDs ensure consistency  
- **Atomic Publication**: SQLite compare-and-swap prevents race conditions
- **Configuration Fingerprinting**: Detects parameter changes between runs
- **Error Recovery**: Graceful failure handling with cleanup 

### Data Integrity
- Progress tracking prevents duplicate processing
- Checkpoint verification ensures reliable enumeration 
- Vector dimension validation prevents corrupted data

## Usage Patterns

### Single Article Ingestion
```bash
python ingest_article.py "Machine Learning"
```

### Bulk Processing (not implemented yet)
The system is designed to work with enumeration scripts that can process multiple articles.

### Monitoring Progress
Check `wikipedia/processing/ingestion/ingestion_progress.db` for tracking information.

## Troubleshooting

### Common Issues

1. **Ollama not responding**:
   - Ensure Ollama service is running
   - Confirm `nomic-embed-text` model is pulled: `ollama pull nomic-embed-text`

2. **Qdrant connection issues**:
   - Verify Qdrant server is accessible at `localhost:6333`
   - Check that the correct collection names are defined

3. **Missing database files**:
   - Database will be created automatically on first run
   - Ensure write permissions in the project directory

### Debugging

Run verification tests to validate your setup:
```bash
python wikipedia/processing/ingestion/final_verification.py
```

## Future Enhancements

The current implementation provides core functionality. Future improvements include:

1. **Bulk processing pipeline** with enumeration checkpointing  
2. **Enhanced error recovery** mechanisms
3. **Performance optimization** for large-scale ingestion
4. **Monitoring and logging** improvements
5. **Integration with conversational interfaces**

## Security Notes

- No external dependencies except local services (Ollama, Qdrant)
- All data stays on the local system
- Configuration fingerprinting prevents accidental parameter changes
- Atomic operations ensure data consistency under failure conditions

---

*This implementation provides a complete, safe, and reliable Wikipedia AI ingestion pipeline that meets all requirements for offline knowledge access.*