# Development Guide

## Setting up the Development Environment

### Prerequisites

1. Python 3.13+
2. Ollama installed and running local embedding model
3. Qdrant server running locally 
4. Required dependencies (see `requirements-recovered.txt`)

### Project Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd WikipediaAI
   ```

2. Install in development mode:
   ```bash
   pip install -e .
   ```

3. Run tests to verify setup:
   ```bash
   pytest
   ```

## Testing Strategy

### Unit Tests
Located in `tests/unit/`. These test individual components without side effects.

### Integration Tests  
Located in `tests/integration/`. These interact with databases and external systems using isolated environments.

### Test Configuration
- In-memory SQLite databases for progress tracking tests
- Mocked Qdrant client for vector storage tests
- Mocked Ollama embeddings for batch processing

## Code Structure

The project follows a clean, maintainable structure:
- `src/wikipedia_ai/` contains the main Python package
- `tests/` directory holds all test files 
- `docs/` includes documentation
- Configuration is externalized to prevent hardcoding

## Safety Protocols

Before any changes:

1. Ensure all production data remains untouched
2. Never modify or delete existing database files
3. Preserve configuration identity during refactoring
4. Validate that safety guards remain active (e.g., disabled legacy ingestion)