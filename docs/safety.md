# Safety Protocols

## Overview

The Wikipedia AI system contains critical production data that must be protected during development and refactoring. This document outlines the safety measures required to prevent accidental data corruption or loss.

## Critical Data Assets

### 1. SQLite Progress Database
- **Location**: `wikipedia/processing/ingestion/ingestion_progress.db`
- **Purpose**: Tracks article processing status, completion, exclusion, and errors
- **Safety Requirement**: Must not be modified or moved during refactoring

### 2. Qdrant Vector Storage  
- **Collections**: Active and test collections containing processed Wikipedia articles
- **Purpose**: Stores vector embeddings and metadata for semantic search
- **Safety Requirement**: Must remain untouched during restructuring

### 3. ZIM Archive 
- **Location**: `wikipedia/downloads/wikipedia_en_all_maxi_2026-08.zim` (~127GB)
- **Purpose**: Contains complete Wikipedia content for processing
- **Safety Requirement**: Must not be moved, modified, or deleted

## Configuration Identity Protection

### Critical Considerations:

1. **Configuration Fingerprints**: Generated from Python source file hashes
2. **Checkpoint Consistency**: Changing module locations affects configuration IDs 
3. **Point ID Determinism**: Qdrant point IDs are deterministic based on configuration
4. **Migration Impact**: Any change to source files included in config fingerprints may invalidate checkpoints

### Safe Refactoring Practices:

- Do not move source files until configuration identity is verified
- Maintain the same import paths from configuration functions and tests
- Preserve module names when possible to keep existing file hashes unchanged
- Test that configuration fingerprints remain stable after refactoring

## Ingestion Safety Guards

### Current Protection Mechanisms:

1. **Legacy Ingestion Disabled**: `ingest_article.py` has a `raise RuntimeError` guard 
2. **Collection Validation**: Explicit checks prevent writing to wrong collections
3. **Configuration Verification**: Fingerprint verification ensures consistent processing  
4. **Progress Tracking**: Atomic operations in SQLite maintain state integrity

## Testing Safety Protocols

### Test Environment Isolation:
- All tests must use in-memory databases or mocked services 
- No database connection tests should touch the production SQLite file
- Mock Qdrant client for vector storage testing (no point ID generation)
- Tests should be marked with appropriate pytest markers (`unit`, `integration`)

### Running Tests:
```bash
# Run only unit tests that don't access production data
pytest tests/unit/ -v

# Run integration tests with isolated databases  
pytest tests/integration/ -v
```

## Prohibited Operations During Restructuring

The following operations must be avoided:

1. **Deleting or modifying** `ingestion_progress.db` 
2. **Altering Qdrant collections** or point IDs
3. **Moving ZIM archive files** 
4. **Modifying Ollama model files**
5. **Changing configuration source filenames**: This affects hash-based fingerprints
6. **Running legacy ingestion scripts** (`ingest_article.py`)
7. **Enabling disabled entry points**
8. **Deleting virtual environment** `.venv`
9. **Upgrading dependencies without verification**

## Emergency Procedures

If an error occurs during development:

1. Revert any uncommitted changes  
2. Check that production database remains intact
3. Verify configuration fingerprints are unchanged
4. Confirm safety guards are still active
5. Document the change for future reference

## Verification Process

Before completing migration:

1. Verify all existing unit tests pass
2. Confirm no production SQLite data was modified
3. Validate safety controls remain functional  
4. Test that existing configuration fingerprints are preserved
5. Ensure legacy ingestion guards remain active