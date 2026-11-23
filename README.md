# Wikipedia AI Pipeline with Open WebUI Integration

This project demonstrates how to create a Wikipedia AI pipeline that can process articles and integrate with Open WebUI for chatting capabilities.

## Project Structure

```
WikipediaAI/
├── src/
│   └── wikipedia_ai/
│       └── ingestion/
│           ├── article_ingestion.py      # Main ingestion logic
│           ├── qdrant_batch.py           # Qdrant upload functionality
│           ├── config.py                 # Configuration handling
│           ├── target.py                 # Collection targeting
│           └── ...                       # Other supporting modules
├── open-webui/                           # Open WebUI directory
│   └── vector_db/
│       └── chroma.sqlite3                # Chroma database used by Open WebUI
├── test_single_article.py                # Test script for single article processing
├── run_single_test.py                    # Run test script
├── qdrant_to_openwebui_export.py         # Export data from Qdrant to Open WebUI format
├── test_pipeline_comprehensive.py        # Comprehensive pipeline testing
└── open_webui_integration.md             # Integration documentation
```

## System Overview

### Wikipedia AI Pipeline
1. **Ingestion Process**: Processes Wikipedia articles from ZIM archives
2. **Content Processing**: Extracts and chunks article content
3. **Embedding Generation**: Creates vector embeddings using Ollama
4. **Storage**: Stores vectors in Qdrant for efficient retrieval

### Open WebUI Integration
- Open WebUI uses Chroma as its vector database
- Our pipeline uses Qdrant for storage
- Bridge created through data export functionality

## Key Components

### 1. Ingestion Pipeline
The main ingestion logic is in `src/wikipedia_ai/ingestion/article_ingestion.py`. It handles:
- Reading from ZIM archives (simulated for testing)
- Content extraction and chunking
- Embedding generation 
- Upload to Qdrant

### 2. Qdrant Integration
Data is stored in Qdrant collections:
- `wikipedia_articles` (ACTIVE_COLLECTION) - For production data
- `wikipedia_test_articles` (TEST_COLLECTION) - For testing data

### 3. Open WebUI Compatibility
The integration solution includes:
- Data export script (`qdrant_to_openwebui_export.py`) to bridge Qdrant and Chroma
- Configuration documentation for Open WebUI setup

## Testing the Pipeline

### Prerequisites
1. Qdrant server running on `http://127.0.0.1:6333`
2. Open WebUI running with Chroma database
3. Python dependencies installed (qdrant-client, wikipedia-api, etc.)

### Test Steps

1. **Run the ingestion test**:
   ```bash
   python run_ingestion_test.py
   ```

2. **Test the complete pipeline**:
   ```bash
   python test_pipeline_comprehensive.py
   ```

3. **Export data for Open WebUI**:
   ```bash
   python qdrant_to_openwebui_export.py
   ```

## Integration with Open WebUI

### Approach 1: Direct Qdrant Connection (Recommended)
Modify Open WebUI's configuration to point directly to your Qdrant instance instead of Chroma.

### Approach 2: Data Export and Import
Use the export script to convert Qdrant data to a format compatible with Chroma, then import it into Open WebUI.

## Configuration

The system uses configuration IDs generated from:
- ZIM file details
- Collection names  
- Embedding model settings
- Vector dimensions

These ensure deterministic and reproducible ingestion processes.

## Troubleshooting

### Common Issues
1. **Qdrant Connection Errors**: Ensure Qdrant server is running on port 6333
2. **Import Errors**: Make sure all Python dependencies are installed
3. **Database Compatibility**: The export script bridges the gap between Qdrant and Chroma formats

### Testing Commands
```bash
# Test basic functionality
python run_ingestion_test.py

# Run comprehensive tests
python test_pipeline_comprehensive.py

# Export data for Open WebUI
python qdrant_to_openwebui_export.py
```

## Future Enhancements

1. **Direct Chroma Integration**: Modify the pipeline to store directly in Chroma
2. **Real-time Sync**: Implement real-time synchronization between Qdrant and Chroma
3. **Improved Error Handling**: More robust error handling and logging
4. **Performance Optimization**: Optimize batch processing for larger datasets

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.