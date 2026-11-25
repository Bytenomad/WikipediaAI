# WikipediaAI Architecture

## Overview

This document describes the architectural design of the WikipediaAI system, including its components, their interactions, and the rationale behind key design decisions. The system has been refactored to improve modularity, scalability, and maintainability.

## System Components

### 1. Core Services (services/ directory)

#### Embedding Service
- **Interface**: `EmbeddingService` (abstract base class)
  - Defines `generate_embeddings(texts: list[str]) -> list[list[float]]`
- **Implementation**: `OllamaEmbeddingService` 
  - Concrete implementation using the Ollama API for embedding generation
  - Configurable model name and base URL

#### Qdrant Service  
- **Interface**: `QdrantService` (abstract base class)
  - Defines `initialize_collection(name: str, vector_size: int, distance: str) -> None`
  - Defines `upload_batch(collection_name: str, records: list[VectorRecord]) -> None`
  - Defines `search(collection_name: str, vector: list[float], limit: int) -> list[VectorRecord]`
- **Implementation**: `QdrantServiceImpl`
  - Concrete implementation using existing Qdrant functionality
  - Handles database operations for vector storage and retrieval

### 2. Configuration Management (config_manager.py)

- Centralized configuration loading with validation
- Environment-based configuration resolution
- Error handling for missing or invalid configurations
- Support for different environments (development, production)

### 3. Ingestion Pipeline (ingestion/ directory)

#### Main Script
- `import_all_us_history.py`: Orchestrates the entire ingestion process
- Uses service abstractions instead of direct implementation
- Manages flow control and coordination between components

#### Supporting Modules
- `batch_embeddings.py`: Processes text in batches for embedding generation 
- `qdrant_batch.py`: Handles batch upload to Qdrant database
- `article_ingestion.py`: Processes individual articles and chunks them for storage

### 4. Data Models (models/ directory)

#### VectorRecord
- Standardized data structure representing vectorized content
- Contains ID, vector data, metadata, and payload
- Used consistently across the system for uniform handling

## Design Patterns

### Service Abstraction Pattern
- Abstract base classes define contracts for services
- Enables multiple implementations with consistent interfaces
- Facilitates easy swapping or extension of service implementations

### Dependency Injection
- Services are injected rather than created internally
- Improves testability and flexibility  
- Reduces tight coupling between components

### Configuration as Code
- Environment variables and configuration files used for settings
- Validated at startup to prevent runtime errors
- Clear separation between code and environment-specific values

## Data Flow

1. **Article Processing**: Articles are fetched from Wikipedia
2. **Text Chunking**: Large articles are divided into manageable chunks  
3. **Embedding Generation**: Text chunks are converted to vector embeddings using Ollama
4. **Qdrant Storage**: Vectors are uploaded to Qdrant database with metadata
5. **Retrieval**: Vector search capabilities enable fast article retrieval

## Benefits of Refactoring

### Modularity
- Clear separation between concerns 
- Easier to understand and maintain individual components
- Independent development and testing of services

### Scalability  
- Service interfaces make it easy to swap implementations (e.g., different embedding models)
- Configuration-driven design supports multiple deployment scenarios

### Maintainability
- Abstract base classes enforce consistent APIs across implementations
- Centralized configuration reduces hard-coded values
- Improved testability with service abstractions

### Testability 
- Services can be mocked for unit testing
- Integration tests verify component interactions
- Clear interfaces make it easier to write comprehensive tests

## Future Enhancements

1. **Additional Qdrant Implementations**: Support different storage backends or configurations  
2. **Alternative Embedding Models**: Add support for other embedding generation services
3. **Performance Monitoring**: Add metrics collection and logging capabilities
4. **Advanced Search Features**: Implement more sophisticated search capabilities

## Key Files and Directories

```
src/wikipedia_ai/
├── ingestion/
│   ├── import_all_us_history.py         # Main orchestration script  
│   ├── batch_embeddings.py              # Embedding generation component
│   ├── qdrant_batch.py                  # Qdrant upload functionality
│   ├── article_ingestion.py             # Article processing logic
│   ├── config_manager.py                # Configuration management  
│   └── services/                        # Service abstractions and implementations
│       ├── __init__.py
│       ├── embedding_service.py         # Embedding service definitions
│       └── qdrant_impl.py               # Qdrant implementation
├── models/
│   └── vector_record.py                 # Data model definitions
├── tests/                               # Unit and integration tests
└── README.md                            # Documentation
```