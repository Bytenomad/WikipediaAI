# Wikipedia AI - Visual Studio Code Development Setup

This document provides complete instructions for setting up the Wikipedia AI project for development and debugging in Visual Studio Code.

## Project Overview

The Wikipedia AI project is a Python-based system that processes Wikipedia content using:
- Offline ZIM archives 
- Local embeddings (Ollama)
- Vector storage (Qdrant)
- Integration with Open WebUI

## Prerequisites

1. **Python 3.13** or higher
2. **Visual Studio Code** with Python extension installed
3. **Qdrant server** running on `http://127.0.0.1:6333`
4. **Ollama** for embedding generation
5. **ZIM archive** of Wikipedia content

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
# Clone repository (if not already done)
git clone <repository-url>
cd WikipediaAI

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install project in development mode
pip install -e .
```

### 2. VS Code Configuration

The project already includes `.vscode` configuration files:

#### File: `.vscode/settings.json`
```json
{
    "python.defaultInterpreterPath": "./.venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false
}
```

#### File: `.vscode/launch.json`
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Python: Test Single Article",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/test_single_article.py",
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Python: Ingestion Test",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/run_ingestion_test.py",
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Python: Comprehensive Pipeline Test",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/test_pipeline_comprehensive.py",
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
```

### 3. Running and Debugging

1. **Open in VS Code**:
   ```
   code .
   ```

2. **Set breakpoints** in any Python file (like `test_single_article.py`)

3. **Use the debug dropdown** to select a configuration:
   - Python: Current File
   - Python: Test Single Article
   - Python: Ingestion Test
   - Python: Comprehensive Pipeline Test

4. **Press F5** or click the debug button to start debugging

### 4. Available Test Scripts

- `test_single_article.py` - Single article processing test
- `run_ingestion_test.py` - Basic ingestion tests  
- `test_pipeline_comprehensive.py` - Full pipeline test
- `qdrant_to_openwebui_export.py` - Open WebUI integration export

## Verification

To verify your setup is working correctly:

1. Run the verification script:
   ```bash
   python verify_setup.py
   ```

2. Or open any Python file in VS Code and use the debug configurations.

## Troubleshooting

If you encounter issues with the launch.json file, ensure it's properly formatted as JSON with boolean values as `true` (not "true" or 'true').

The setup is now complete and ready for development and debugging of the Wikipedia AI pipeline.