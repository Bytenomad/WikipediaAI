# Wikipedia AI

This project enables importing Wikipedia articles into Qdrant for retrieval-augmented generation (RAG) with support for offline image functionality.

## Features

- Import Wikipedia articles in batches to manage memory usage
- Extract and store images locally for offline functionality
- Integration with Qdrant vector database
- Integration with Open WebUI for chat interface
- Support for category-based article imports

## Architecture

```
Wikipedia ZIM → Chunking → Image Extraction → Qdrant Upload → Open WebUI
     ↑                                    ↓
     └─ Local Image Storage (./open-webui/uploads/images) 
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download the Wikipedia ZIM file to `wikipedia/downloads/` directory

3. Configure Docker with proper volume mounts

## Usage

### Importing Articles

#### 1. Full Ingestion (All Articles)
```bash
python src/wikipedia_ai/ingestion/run_full_ingestion.py
```

#### 2. Category-Based Import
```bash
# Import articles from a specific category in batches
python src/wikipedia_ai/ingestion/import_category_batch.py "Medicine" 5

# Import articles from the "Science" category with default batch size
python src/wikipedia_ai/ingestion/import_category_batch.py "Science"
```

### Docker Configuration

```bash
docker compose up -d
```

The Compose file defaults `WIKIPEDIA_ZIM_DIR` to
`D:/WikipediaAI/wikipedia/downloads` for this setup. Set that environment
variable to your host's ZIM directory before starting Compose if it is stored
elsewhere.

### Tests

Automated tests live under `tests/unit`, `tests/integration`, and `tests/`. Older
service-dependent checks are kept in `tests/manual/` and are excluded from normal
pytest runs; run those individually from the repository root when their services
and data are available.

## Key Components

1. **Chunking**: Splits articles into manageable text chunks
2. **Image Extraction**: Extracts images from Wikipedia articles and saves them locally
3. **Qdrant Integration**: Stores article chunks with embeddings in Qdrant
4. **Response Formatting**: Formats responses for Open WebUI display with image references
5. **Category Import**: New functionality to import specific article categories

## Directory Structure

```
.
├── wikipedia/
│   └── downloads/                 # Wikipedia ZIM files
├── open-webui/
│   ├── vector_db/                 # Chroma database
│   └── uploads/images/            # Local image storage for offline use
├── data/
│   └── qdrant/                    # Qdrant data directory
└── src/
    └── wikipedia_ai/
        ├── ingestion/             # Main ingestion scripts
        │   ├── chunking.py        # Text chunking functionality
        │   ├── image_extraction.py # Image extraction from HTML
        │   ├── response_formatter.py # Format responses for Open WebUI
        │   ├── qdrant_batch.py    # Qdrant batch upload
        │   ├── run_full_ingestion.py # Main ingestion workflow
        │   └── import_category_batch.py # Category-based import script
        └── config.py              # Configuration settings
```

## Docker Setup

The Docker configuration mounts the necessary directories for:
- ZIM file access
- Qdrant data persistence
- Open WebUI database and uploads
- Local image storage for offline access

## Testing

Run tests to verify functionality:
```bash
python tests/test_category_import.py
```

## Troubleshooting

### ZIM Path Issues

If you encounter ZIM path issues in Docker, ensure:
1. The ZIM file is in `wikipedia/downloads/` directory
2. The Docker volume mounts are correctly configured
3. Set the `ZIM_PATH` environment variable if needed

### Image Storage

Images are automatically saved to `./open-webui/uploads/images/` and referenced in Qdrant for Open WebUI display.

## Future Work

- Improve category filtering in ZIM file
- Add support for more Wikipedia content types
- Implement incremental updates to existing collections
