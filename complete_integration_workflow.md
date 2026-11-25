# Complete Integration Workflow: Wikipedia AI to Open WebUI

## Current System Status

Based on our analysis, the system architecture is:
- Uses Qdrant for vector storage 
- Has an export script designed to convert data for Open WebUI compatibility
- Requires Wikipedia ZIM files for content processing
- Currently lacks actual Wikipedia content due to missing ZIM files

## Issues Identified

1. **Missing ZIM Files**: The hardcoded path in `chunking.py` points to a non-existent file
2. **Incomplete Ingestion Process**: Tests only simulate, don't execute actual upload
3. **Path Configuration**: Hardcoded paths don't work in different environments

## Step-by-Step Integration Solution

### Step 1: Prepare ZIM File
First, obtain a Wikipedia ZIM archive:
- Download from [Kiwix archives](https://download.kiwix.org/zim/wikipedia/)
- Example file: `wikipedia_en_all_maxi_2026-08.zim`
- Place it in a known location

### Step 2: Update Configuration
Update the ZIM path in `chunking.py`:

```python
# In src/wikipedia_ai/ingestion/chunking.py, line 20:
ZIM_PATH = Path(r"C:\path\to\your\wikipedia_en_all_maxi_2026-08.zim")
```

### Step 3: Test End-to-End Workflow

Create a test script that demonstrates the full workflow:

```python
#!/usr/bin/env python3
"""
Complete end-to-end test for Wikipedia AI to Open WebUI integration.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Import modules
from qdrant_batch import QdrantClient
from config import configuration_id
from chunking import process_article
from qdrant_to_openwebui_export import export_from_qdrant

def test_complete_workflow():
    """Test the complete workflow from article processing to Open WebUI export."""
    
    print("=== Testing Complete Workflow ===")
    
    # 1. Check Qdrant connection
    try:
        client = QdrantClient(url="http://127.0.0.1:6333")
        collections = [col.name for col in client.get_collections().collections]
        print(f"Qdrant available, collections: {collections}")
    except Exception as e:
        print(f"Qdrant connection failed: {e}")
        return False
    
    # 2. Test article processing (this will actually work now with proper ZIM)
    try:
        print("Processing test article...")
        result = process_article("Testville")
        print(f"Article processed successfully: {result}")
    except Exception as e:
        print(f"Article processing failed: {e}")
        return False
    
    # 3. Export to Open WebUI format
    try:
        print("Exporting to Open WebUI format...")
        exported_data = export_from_qdrant()
        print(f"Exported {len(exported_data)} documents")
        
        # Save to file for Open WebUI import
        with open('qdrant_export.json', 'w') as f:
            import json
            json.dump(exported_data, f, indent=2)
        print("Export saved to qdrant_export.json")
        
    except Exception as e:
        print(f"Export failed: {e}")
        return False
    
    print("=== Workflow Test Completed Successfully ===")
    return True

if __name__ == "__main__":
    test_complete_workflow()
```

### Step 4: Run the Integration Process

1. **Start Qdrant** (if not already running):
```bash
# If using Docker:
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

2. **Run the full workflow**:
```bash
cd D:\source\repos\WikipediaAI
python complete_integration_workflow.py
```

### Step 5: Configure Open WebUI

1. Set up Chroma database in Open WebUI
2. Import the exported data from `qdrant_export.json`
3. Configure your Open WebUI application to use this database

## Expected Results

After successful execution, you should see:
- Articles processed and stored in Qdrant
- Exported JSON file compatible with Open WebUI's Chroma format
- Working integration between Wikipedia AI pipeline and Open WebUI

## Troubleshooting

If you encounter issues:

1. **ZIM File Not Found**: Ensure the ZIM file exists at the specified path
2. **Qdrant Connection Issues**: Verify Qdrant is running on port 6333
3. **Import Errors**: Make sure all Python dependencies are installed:
```bash
pip install qdrant-client libzim
```

This workflow provides a complete solution for integrating your Wikipedia AI pipeline with Open WebUI, addressing all the configuration and path issues identified.