# US History Content Import Functionality

This document describes the implementation of US history content import functionality for the Wikipedia AI system.

## Overview

The system has been extended to support importing US history content from Wikipedia ZIM files using the existing category-based import approach. This functionality allows users to specifically target and import articles related to US history topics.

## Implemented Categories

The following major US history categories are supported:
- Category:United_States
- Category:History_of_the_United_States  
- Category:American_Civil_War
- Category:American_Revolution

## Scripts Available

### 1. `import_us_history.py`
Imports content from a specific US history category.

Usage:
```bash
python import_us_history.py "Category Name" batch_size
```

### 2. `import_all_us_history.py` 
Imports content from all major US history categories.

Usage:
```bash
python import_all_us_history.py batch_size
```

## Technical Implementation

### Key Features
- **Category-based Import**: Uses the existing category system to access articles
- **Docker Compatible**: Properly configured for containerized environments
- **Image Support**: Extracts and handles images from Wikipedia articles
- **Batch Processing**: Efficient memory usage with configurable batch sizes
- **Error Handling**: Robust error handling that gracefully skips missing articles

### Integration Points
- **Qdrant Storage**: Content is stored in Qdrant database collections
- **Open WebUI**: Integrated with Open WebUI for display and chat functionality
- **Chunking**: Proper text chunking for efficient storage and retrieval

## Docker Configuration

The system properly mounts the ZIM file directory in Docker containers:
```yaml
volumes:
  - ./wikipedia/downloads:/app/wikipedia/downloads
```

## Testing Results

All import functionality has been thoroughly tested and verified to:
- Access Wikipedia ZIM files correctly
- Retrieve articles from US history categories
- Process articles with proper chunking and image handling
- Upload content to Qdrant successfully
- Integrate seamlessly with Open WebUI

## Usage Example

To import all US history content:
```bash
python import_all_us_history.py 10
```

To import from a specific category:
```bash
python import_us_history.py "History of the United States" 5
```