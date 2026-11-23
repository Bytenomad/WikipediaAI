# Wikipedia AI to Open WebUI Integration Plan

## Overview
This document outlines a complete implementation plan for integrating the Wikipedia AI pipeline with Open WebUI, addressing all identified issues and providing clear next steps.

## Phase 1: Environment Setup

### 1.1 Download Wikipedia ZIM Archive
- Visit https://download.kiwix.org/zim/wikipedia/
- Download a recent English Wikipedia ZIM file (e.g., `wikipedia_en_all_maxi_2026-08.zim`)
- Place the file in: `C:\wikipedia\downloads\`

### 1.2 Update Configuration
Edit `src/wikipedia_ai/ingestion/chunking.py`:
```python
# Change line 20 from:
ZIM_PATH = Path(r"D:\WikipediaAI\wikipedia\downloads\wikipedia_en_all_maxi_2026-08.zim")
# To:
ZIM_PATH = Path(r"C:\wikipedia\downloads\wikipedia_en_all_maxi_2026-08.zim")
```

### 1.3 Verify Qdrant Setup
Ensure Qdrant is running:
```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

## Phase 2: Data Ingestion

### 2.1 Run Full Ingestion Process
```bash
cd C:\Users\Main\source\repos\WikipediaAI
python run_full_ingestion.py
```

This will process articles from the ZIM file and store them in Qdrant.

### 2.2 Verify Data Storage
Check that data is properly stored in Qdrant:
```bash
curl http://localhost:6333/collections
```

## Phase 3: Export for Open WebUI

### 3.1 Export Data
The export script should automatically run during ingestion, but can also be executed manually:
```bash
python src/wikipedia_ai/ingestion/qdrant_to_openwebui_export.py
```

This generates `qdrant_export.json` in the working directory.

## Phase 4: Open WebUI Configuration

### 4.1 Setup Chroma Database
In Open WebUI, configure a new Chroma database:
- Create a new database connection
- Set up appropriate collection names matching your Qdrant data

### 4.2 Import Exported Data
Import the `qdrant_export.json` file into Open WebUI's Chroma database.

### 4.3 Configure Chat Interface
Set up Open WebUI to use this database for chat functionality:
- Configure the model and parameters
- Set appropriate context window sizes

## Phase 5: Testing and Validation

### 5.1 Test Chat Functionality
- Start a chat session in Open WebUI
- Ask questions about Wikipedia content
- Verify responses are based on the imported data

### 5.2 Validate Data Consistency
- Compare article content between Qdrant and Open WebUI
- Ensure no data loss during conversion process

## Phase 6: Optimization and Documentation

### 6.1 Make Paths Configurable
Update `chunking.py` to use environment variables or config files:
```python
import os
ZIM_PATH = Path(os.getenv('WIKIPEDIA_ZIM_PATH', 'default_path'))
```

### 6.2 Add Error Handling
Implement graceful error handling for missing files and connection issues.

### 6.3 Create Setup Script
Develop an automated setup script that handles all configuration steps.

## Expected Outcome
After completing this integration plan, you will have a fully functional Wikipedia AI pipeline that feeds content into Open WebUI for chat-based interaction, with data flowing seamlessly from Wikipedia articles through Qdrant storage to Chroma database format compatible with Open WebUI.