# Wikipedia AI Development Instructions

## Project Overview

This is a Wikipedia AI project that processes offline Wikipedia content using ZIM archives, local embeddings (Ollama), and Qdrant vector storage. 

## Safety Protocols

### Critical Data Protection
- **DO NOT DELETE OR MODIFY**: `wikipedia/processing/ingestion/ingestion_progress.db` 
- **DO NOT DELETE OR MOVE**: Wikipedia ZIM archive `wikipedia/downloads/wikipedia_en_all_maxi_2026-08.zim`
- **DO NOT ALTER**: Qdrant collection structure or existing point IDs
- **DO NOT DELETE OR MODIFY**: Ollama model files
- **DO NOT RUN**: Legacy ingestion scripts (`ingest_article.py`)
- **DO NOT ENABLE**: Disabled ingestion entry points

### Configuration Fingerprinting Criticality
The system uses source file hashes for generating configuration fingerprints. Moving or changing Python modules may:
- Invalidate existing checkpoints 
- Cause point ID mismatches in Qdrant 
- Break the resumable processing capability

## Development Guidelines

1. **Testing**: All tests must be isolation-focused (in-memory DBs, mocked services)
2. **Python Structure**: Use modern `src/` layout with proper package imports
3. **Documentation**: Keep all documentation current with code changes  
4. **Git Safety**: No production data should be committed to Git

## Project Structure 

```
C:\WikipediaAI\
├── src\wikipedia_ai\          # Main Python package
├── tests\                     # Unit/integration tests 
├── docs\                      # Documentation files
├── wikipedia\                 # Runtime data (ZIM archives, etc.)
├── .vscode\                   # VS Code development configuration
└── pyproject.toml             # Package configuration for pip install -e .
```

## Key Modules

- `wikipedia_ai.ingestion.article_ingestion`: Main processing pipeline
- `wikipedia_ai.ingestion.chunking`: HTML parsing and content splitting  
- `wikipedia_ai.ingestion.batch_embeddings`: Ollama embedding generation
- `wikipedia_ai.ingestion.qdrant_batch`: Vector storage operations
- `wikipedia_ai.ingestion.progress_tracking`: SQLite tracking system

## Testing Approach

- Unit tests: Module behavior without external dependencies  
- Integration tests: Database and service interactions with isolated environments
- All tests should pass with minimal environmental assumptions

## Environment Setup

Python environment located at: 
`C:\WikipediaAI\wikipedia\processing\ingestion\.venv`

The system uses:
- Ollama as local embedding server
- Qdrant for vector storage  
- SQLite for progress tracking