# Ingestion Lifecycle

## Overview

The Wikipedia AI system processes Wikipedia articles through a well-defined lifecycle that ensures data integrity, progress tracking, and safe resumption of interrupted processing.

## Processing Steps

### 1. Enumeration
- Enumerates articles from ZIM archive using `enumerate_articles.py`  
- Filters out redirects, meta-refresh redirects, and disambiguation pages
- Provides iterator for article titles and paths

### 2. Content Parsing
- Opens HTML entries in the ZIM archive
- Uses BeautifulSoup to parse content with lxml parser
- Filters out non-prose content (tables, images, metadata, etc.)
- Removes excluded sections (references, notes, external links)

### 3. Paragraph Chunking  
- Splits content into paragraph-sized chunks
- Maintains section boundaries where possible
- Ensures each chunk is within the configured character limit (MAX_CHARS)
- Preserves original text to ensure content integrity

### 4. Embedding Generation
- Uses local Ollama embedding model (nomic-embed-text) 
- Processes text batches for efficient encoding
- Generates vectors of consistent dimensions (768)

### 5. Vector Storage  
- Uploads chunks to Qdrant with deterministic point IDs
- Point IDs are generated based on configuration + article path + chunk index
- Collections are clearly separated (ACTIVE vs TEST)
- Handles batch uploads with error recovery

### 6. Progress Tracking
- Updates SQLite database with processing status
- Tracks completion, errors, exclusions, and attempts
- Enables resumable processing from interruption points
- Maintains artifact counts for monitoring

### 7. Cleanup Operations  
- Removes stale chunks when articles are updated
- Handles article exclusions appropriately
- Proper error handling during cleanup operations  

## Checkpoint Management

The system uses multiple checkpoint files to enable resumable ingestion:

### Configuration Fingerprinting 
- Calculates SHA-256 hash of key configuration components  
- Components include: ZIM file, collection name, embedding model, chunking settings
- Source code hashes for: chunking module, embedding module, Qdrant upload module

### Progress Database
- `ingestion_progress.db` tracks article status through processing lifecycle
- Each article has a unique record tied to its configuration ID
- Supports retry and resumption capabilities  

## Safety Protocols

### Protection Measures:
1. **Legacy Ingestion Disabled**: Prevents accidental data corruption
2. **Atomic Operations**: SQLite transactions ensure consistency
3. **Configuration Validation**: Fingerprint checking prevents mismatched processing 
4. **Collection Isolation**: TEST vs ACTIVE collections prevent cross-contamination

## Error Handling

### Common Failure Points:
1. **Network Issues**: Connection to Ollama or Qdrant
2. **Database Locks**: Concurrent access to SQLite progress tracking  
3. **Content Parsing**: Malformed HTML content in ZIM archive
4. **Memory Constraints**: Large article processing 

### Recovery Mechanisms:
- Article status transitions through "processing" → "completed"/"failed"/"excluded"
- Retries on recoverable errors  
- Proper cleanup during failure conditions
- Logging of failure details for debugging

## Resumable Processing

The system supports interruption/restart scenarios:

1. **Checkpoint Persistence**: Progress tracked in SQLite database
2. **Duplicate Prevention**: Configuration fingerprints prevent reprocessing same content identically  
3. **Incremental Updates**: Stale chunks are removed when updating articles
4. **Status Restoration**: Process continues from last known good state