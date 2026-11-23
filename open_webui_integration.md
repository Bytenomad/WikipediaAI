# Open WebUI Integration for Wikipedia AI

## Current System Overview

The Wikipedia AI pipeline:
1. Processes Wikipedia articles from ZIM archives
2. Generates embeddings locally using Ollama
3. Stores vectors in Qdrant for efficient retrieval
4. Has a resumable ingestion process with progress tracking

## Integration Challenges

Open WebUI uses Chroma as its vector database, but our pipeline uses Qdrant. We need to bridge this gap.

## Solutions

### Option 1: Configure Open WebUI to use Qdrant
- Modify Open WebUI's vector database configuration to point to our Qdrant instance
- This requires understanding Open WebUI's configuration structure

### Option 2: Export Qdrant data to Chroma format
- Create a script to export data from Qdrant to a format compatible with Chroma
- This allows Open WebUI to work with the existing data

### Option 3: Use both databases simultaneously
- Store data in both Qdrant (for pipeline) and Chroma (for Open WebUI)
- Requires modifications to the ingestion process

## Implementation Plan

1. **Verify Qdrant connection** - Ensure our pipeline can connect to Qdrant
2. **Create a data export script** - Export Qdrant data for Open WebUI usage
3. **Modify Open WebUI configuration** - Point it to our Qdrant instance or import the data
4. **Test the complete workflow** - From ingestion to chat in Open WebUI

## Testing Steps

1. Run single article ingestion test
2. Verify data is stored in Qdrant
3. Export data for Open WebUI compatibility
4. Configure Open WebUI to use the data
5. Test chat functionality with the article content

## Configuration Details

### Current Qdrant Setup
- Collection names: `wikipedia_articles` (ACTIVE_COLLECTION) and `wikipedia_test_articles` (TEST_COLLECTION)
- Vector dimensions: 768
- Embedding model: nomic-embed-text

### Open WebUI Database
- Uses Chroma with `chroma.sqlite3` database file
- Structure needs to be compatible with our Qdrant data format

## Next Steps

1. Test the existing ingestion pipeline with a single article
2. Verify that data is correctly stored in Qdrant
3. Implement the export functionality to bridge Qdrant and Chroma
4. Configure Open WebUI to work with the exported data