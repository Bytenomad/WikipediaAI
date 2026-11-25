# WikipediaAI - Advanced Refactoring

## Overview
This repository contains an implementation of Wikipedia article ingestion and vector search using Qdrant and Ollama. The system has been refactored for improved modularity, scalability, and maintainability.

## Architecture
The system now follows a service-oriented architecture with:

1. **Abstract Service Interfaces**: Defined in `services/` directory for embedding and Qdrant operations
2. **Concrete Implementations**: Specific implementations using Ollama and existing Qdrant capabilities  
3. **Configuration Management**: Centralized configuration with validation (`config_manager.py`)
4. **Modular Design**: Separation of concerns throughout the ingestion pipeline

## Key Refactorings Implemented

### Service Abstractions
- `EmbeddingService` (abstract base class): Defines interface for embedding generation
- `OllamaEmbeddingService`: Concrete implementation using Ollama
- `QdrantService` (abstract base class): Defines interface for Qdrant operations  
- `QdrantServiceImpl`: Concrete implementation using existing Qdrant functionality

### Configuration Management
- Centralized configuration loading with validation
- Environment-based configuration resolution
- Error handling for missing or invalid configurations

### Pipeline Components
- Updated ingestion script (`import_all_us_history.py`) to use service abstractions
- Refactored batch processing components (`batch_embeddings.py`, `qdrant_batch.py`)
- Maintained backward compatibility while improving testability

## Getting Started

1. **Requirements**: Install requirements.txt using `pip install -r requirements.txt`
2. **Docker Setup**: Run `docker-compose up` to start dependencies (Qdrant, Ollama)
3. **Configuration**: Set environment variables for your system configuration
4. **Run Ingestion**: Execute the main script with `python import_all_us_history.py`

## Testing

The module includes unit tests for service abstractions that verify:
- Service instantiation and method availability
- Configuration loading and validation
- Basic integration between components

Run tests with: `python -m unittest discover -s src/wikipedia_ai/ingestion/tests -v`

## Documentation

- `ARCHITECTURE.md`: Detailed architectural design
- This README: Overview of usage and implementation

## Contributing

Contributions are welcome! Please:
1. Fork the repository  
2. Create a feature branch
3. Make your changes with appropriate tests
4. Submit a pull request
