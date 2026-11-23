# Wikipedia AI

This project provides tools for importing and processing Wikipedia articles for use in AI applications, particularly with Open WebUI integration.

## Key Features

- Import Wikipedia articles from multiple categories (US History in this case)
- Generate embeddings using local Ollama API
- Store data in Qdrant vector database
- Process articles into chunks for better retrieval

## Architecture

The system consists of several key modules:
1. `batch_embeddings.py` - Generates embeddings for text batches using Ollama
2. `import_all_us_history.py` - Main script to import US History Wikipedia categories
3. `qdrant_batch.py` - Handles batch uploading to Qdrant database
4. `target.py` - Defines valid collection names for Qdrant integration

## Usage

### Prerequisites
- Local Ollama installation with `nomic-embed-text` model
- Qdrant database running locally
- Wikipedia ZIM file in the expected location

### Running Import
```bash
python src/wikipedia_ai/ingestion/import_all_us_history.py [batch_size]
```

### Example
```bash
python src/wikipedia_ai/ingestion/import_all_us_history.py 5
```

## Key Fixes Implemented

1. **Ollama API Response Format**: Fixed handling of single 'embedding' key instead of batched 'embeddings' key
2. **Import Script Integration**: Resolved parameter passing issues with Qdrant upload functions
3. **Collection Naming**: Fixed usage of TEST_COLLECTION constant

The system now works correctly with Ollama's API behavior where each text gets its own separate embedding call.