# Wikipedia AI Pipeline with Open WebUI Integration

This project implements a complete Wikipedia AI pipeline that integrates with Open WebUI for chat functionality, including support for Wikipedia images.

## Overview

The system processes Wikipedia articles from ZIM files, creates vector embeddings using Qdrant for storage, and makes the content available to Open WebUI through Chroma database integration. The implementation includes both text and image support from Wikipedia articles.

## Architecture

```
Wikipedia ZIM → Ingestion Pipeline → Qdrant Vector DB → Open WebUI
    ↑                                               ↓
    └── Image Extraction ←─────────────────────────┘
```

## Key Components

### 1. Wikipedia AI Pipeline
- **Batched Ingestion**: Processes Wikipedia articles from ZIM files in batches
- **Chunking & Embedding**: Splits content into chunks and generates embeddings
- **Qdrant Integration**: Stores vector data in Qdrant database
- **Chroma Compatibility**: Exports data to Chroma format for Open WebUI

### 2. Image Support
- **Image Extraction Module**: `src/wikipedia_ai/ingestion/image_extraction.py`
- **Integration**: Processes images from Wikipedia articles during ingestion
- **Batched Imports**: Handles both text and image content in batch processing

### 3. Open WebUI Integration
- **Database Connection**: Connects to Chroma database containing Wikipedia data
- **Docker Configuration**: Properly configured with volume mappings
- **Version**: Updated to 0.13.4 to resolve update notices

## System Requirements

- Docker and Docker Compose
- Python 3.8+
- At least 4GB RAM for optimal performance
- Internet connection for initial setup

## Setup Instructions

### Prerequisites
1. Install Docker Desktop
2. Clone this repository
3. Download Wikipedia ZIM file to `wikipedia/downloads/`

### Running the System
```bash
# Start all containers
docker-compose -f docker-compose-openwebui-fixed.yml up -d

# Verify containers are running
docker ps

# Access Open WebUI at http://localhost:8081
```

## Usage

1. **Access Open WebUI**: Navigate to http://localhost:8081
2. **Create Chat Session**: Start a new conversation
3. **Ask Questions**: Query about Wikipedia topics (e.g., "What is medicine?")
4. **View Responses**: Both text and image content should display properly

## Key Files

- `docker-compose-openwebui-fixed.yml` - Main Docker configuration
- `open-webui/vector_db/chroma.sqlite3` - Chroma database with Wikipedia data
- `src/wikipedia_ai/ingestion/image_extraction.py` - Image processing module
- `src/wikipedia_ai/ingestion/batched_ingestion.py` - Batched import module

## Testing

The system has been thoroughly tested and verified:
- ✅ All integration components working properly
- ✅ Database connection verified 
- ✅ Text and image content display confirmed
- ✅ Open WebUI chat functionality with Wikipedia data

## Performance Features

- **Batched Processing**: Efficient memory usage for large Wikipedia datasets
- **Scalable Architecture**: Designed to handle extensive Wikipedia content
- **Optimized Chunking**: Balanced text chunk sizes for optimal search results

## Troubleshooting

If you encounter issues:
1. Check that all Docker containers are running: `docker ps`
2. Verify database exists: `ls open-webui/vector_db/chroma.sqlite3`
3. Ensure ZIM file is in the correct location: `wikipedia/downloads/`

## Support

For questions or issues, please check the documentation or contact the development team.

---
*System ready for use at http://localhost:8081*