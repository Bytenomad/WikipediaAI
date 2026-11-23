# Wikipedia AI to Open WebUI Integration Guide

This document describes how to integrate the Wikipedia AI pipeline with Open WebUI's chat interface, specifically addressing the compatibility between Qdrant (used by Wikipedia AI) and Chroma (used by Open WebUI).

## Overview

The Wikipedia AI system uses Qdrant for vector storage with Ollama for embeddings, while Open WebUI uses Chroma as its vector database. This guide explains how to bridge these systems to enable chatting with Wikipedia articles through Open WebUI.

## Current Architecture

### Wikipedia AI Pipeline
- **Data Source**: Wikipedia ZIM files
- **Processing**: Article ingestion, chunking, embedding generation
- **Storage**: Qdrant (vector database)
- **Embeddings**: Ollama (nomic-embed-text model)

### Open WebUI
- **Storage**: Chroma (vector database)
- **Interface**: Web-based chat interface

## Integration Workflow

### 1. Ingestion Process
```bash
# Run the article ingestion script
python src/wikipedia_ai/ingestion/article_ingestion.py "Article Title"
```

This processes an article and stores it in Qdrant.

### 2. Data Export for Open WebUI
The system provides functionality to export data from Qdrant to a format compatible with Open WebUI:

```bash
# Export data from Qdrant
python src/wikipedia_ai/ingestion/qdrant_to_openwebui_export.py
```

This creates a JSON file containing the documents in a format that can be imported into Chroma.

### 3. Import into Open WebUI Chroma
To import the exported data into Open WebUI's Chroma database, you would need to:

1. Run the export script to create a JSON file
2. Create a script that reads this file and imports into Chroma
3. Configure Open WebUI to use this database

## Technical Details

### Qdrant Data Structure
Documents in Qdrant contain:
- `id`: Unique identifier
- `text`: Content of the chunk
- `title`: Article title
- `source`: Source information
- `vector`: Embedding vector (768 dimensions)

### Open WebUI Format Requirements
Open WebUI expects documents with:
- `id`: Document ID
- `content`: Text content
- `metadata`: Additional information including title and source

## Testing the Integration

### Run Single Article Test
```bash
python src/wikipedia_ai/ingestion/test_single_article_final.py
```

This validates the ingestion process works correctly.

### Test Qdrant Export
```bash
python src/wikipedia_ai/ingestion/qdrant_to_openwebui_export.py
```

This verifies that data can be exported from Qdrant in a compatible format.

### Run Integration Demo
```bash
python src/wikipedia_ai/ingestion/openwebui_qdrant_integration.py
```

This demonstrates the complete integration workflow.

## Configuration

### Environment Variables
Make sure the following environment variables are set:
- `QDRANT_HOST`: Host for Qdrant server (default: localhost)
- `QDRANT_PORT`: Port for Qdrant server (default: 6333)

### Ollama Setup
Ensure Ollama is running with the nomic-embed-text model:
```bash
ollama pull nomic-embed-text
```

## Limitations and Considerations

1. **Database Compatibility**: Direct database migration isn't possible due to different storage formats between Qdrant and Chroma.

2. **Vector Dimensionality**: Both systems use 768-dimensional vectors, which is compatible.

3. **Data Format Conversion**: The export script converts between the two formats.

4. **Performance**: For large datasets, consider batch processing during export.

## Future Improvements

1. **Direct Integration**: Develop a plugin or adapter that allows direct connection between Qdrant and Open WebUI's Chroma.

2. **Automated Migration**: Create scripts that automatically sync data between the systems.

3. **Real-time Sync**: Implement real-time synchronization of new articles between systems.

## Troubleshooting

### Common Issues
1. **Connection Failed to Qdrant**: Ensure Qdrant server is running and accessible.
2. **Ollama Not Found**: Verify Ollama is installed and the nomic-embed-text model is pulled.
3. **Import Errors**: Check that the exported JSON format matches Open WebUI expectations.

### Testing Commands
```bash
# Test Qdrant connection
python -c "from wikipedia_ai.ingestion.qdrant_batch import get_client; print(get_client().health_check())"

# Test embedding generation
python -c "from wikipedia_ai.ingestion.batch_embeddings import embed_batch; print(embed_batch(['test']))"
```

## Conclusion

This integration guide provides the framework for using Wikipedia AI articles with Open WebUI's chat interface. While direct database compatibility isn't possible, the export/import approach allows users to leverage the Wikipedia AI pipeline while benefiting from Open WebUI's chat interface.