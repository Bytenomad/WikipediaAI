# Category-Based Wikipedia Import Functionality

## Overview

We have successfully implemented category-based import functionality for Wikipedia articles in the Wikipedia AI system. This feature allows users to import specific categories of articles rather than processing all articles, which is particularly useful for managing memory usage and processing time.

## Implementation Details

### New Script Created
- `src/wikipedia_ai/ingestion/import_category_batch.py` - Main script for category-based imports

### Key Features Implemented
1. **Category Filtering**: The system can now identify and import articles from specific Wikipedia categories
2. **Batch Processing**: Articles are processed in configurable batches to manage memory usage
3. **Image Support**: Category imports maintain full support for image extraction and local storage
4. **Integration**: Works seamlessly with existing Qdrant and Open WebUI integration

### Core Functionality
- `get_articles_from_category()`: Identifies articles within a specified category
- `import_category_batch()`: Processes articles from a category in batches
- Full integration with existing chunking, image extraction, and Qdrant upload processes

## Usage Examples

```bash
# Import articles from the "Medicine" category with batch size of 5
python src/wikipedia_ai/ingestion/import_category_batch.py "Medicine" 5

# Import articles from the "Science" category with default batch size (10)
python src/wikipedia_ai/ingestion/import_category_batch.py "Science"

# Import articles from the "History" category with custom batch size
python src/wikipedia_ai/ingestion/import_category_batch.py "History" 15
```

## Technical Implementation

The implementation follows the same workflow as the full ingestion process:
1. Opens ZIM archive
2. Identifies articles in the specified category
3. Processes each article through chunking
4. Extracts images and saves them locally
5. Formats responses for Open WebUI display
6. Uploads to Qdrant database

## Configuration

The system uses the same `ZIM_PATH` environment variable configuration as other scripts:
```bash
export ZIM_PATH=/path/to/your/wikipedia.zim
python src/wikipedia_ai/ingestion/import_category_batch.py "Category Name"
```

## Docker Integration

The category import functionality works correctly with the Docker configuration that mounts:
- Wikipedia ZIM file directory
- Local image storage directory (`./open-webui/uploads/images`)
- Qdrant data persistence

## Testing

The category import functionality has been tested and verified to work correctly:
- Module imports successfully without errors
- Full workflow integration confirmed
- Image extraction and storage works with category imports
- Batch processing functions correctly
- Integration with existing Qdrant and Open WebUI components maintained

## Benefits

1. **Memory Efficiency**: Process articles in smaller batches to manage memory usage
2. **Targeted Importing**: Focus on specific topics or categories of interest
3. **Offline Support**: All images are stored locally for offline access
4. **Consistent Workflow**: Maintains compatibility with existing system components
5. **Scalable**: Can handle large Wikipedia collections by focusing on specific areas

## Future Enhancements

While the core functionality is complete, future work could include:
- More sophisticated category filtering in ZIM files
- Support for multiple categories in a single import
- Incremental updates to existing category collections
- Performance optimizations for large category imports