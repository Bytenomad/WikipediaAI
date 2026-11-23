# Category-Based Wikipedia Import Usage

This document explains how to use the new category-based import functionality for Wikipedia articles.

## Overview

The category-based import system allows you to import specific batches of Wikipedia articles from particular categories, rather than importing all articles. This approach is more efficient and allows for better organization of your knowledge base.

## Using the Import Script

### Basic Usage

```bash
python src/wikipedia_ai/ingestion/import_category_batch.py <category_name> [batch_size]
```

**Example:**
```bash
# Import articles from the "Medicine" category in batches of 5
python src/wikipedia_ai/ingestion/import_category_batch.py "Medicine" 5

# Import articles from the "Science" category with default batch size (10)
python src/wikipedia_ai/ingestion/import_category_batch.py "Science"
```

### Script Parameters

- `category_name` (required): The name of the Wikipedia category to import articles from
- `batch_size` (optional, default: 10): Number of articles to process in each batch

## How It Works

1. **ZIM Archive Access**: The script opens the Wikipedia ZIM file using libzim
2. **Category Filtering**: It identifies articles belonging to the specified category
3. **Batch Processing**: Articles are processed in configurable batches to manage memory usage
4. **Content Extraction**: For each article:
   - Extracts HTML content
   - Processes chunks of text for database storage
   - Extracts images from the article
5. **Image Handling**: Images are saved locally in `./open-webui/uploads/images/`
6. **Database Upload**: Processed articles are uploaded to Qdrant with image references
7. **Response Formatting**: Formats responses properly for Open WebUI display with image references

## Requirements

- Wikipedia ZIM file located at `D:\WikipediaAI\wikipedia\downloads\wikipedia_en_all_maxi_2026-08.zim`
- Proper Docker configuration with volume mounts for images
- Existing Qdrant and Open WebUI setup

## Troubleshooting

### Common Issues

1. **ZIM File Path Error**: If the script can't find the ZIM file, ensure it's in the correct location or update the `ZIM_PATH` in `chunking.py`.

2. **Category Not Found**: The category search might not work as expected with the current implementation. You may need to adjust how categories are identified in the ZIM file.

3. **Memory Issues**: For large categories, consider reducing the batch size to manage memory usage.

### Testing

Run the test script to verify functionality:

```bash
python tests/test_category_import.py
```

## Integration with Existing System

This new import functionality integrates seamlessly with:
- Existing image extraction and storage
- Qdrant database upload process
- Open WebUI response formatting
- Docker volume mounting for local images