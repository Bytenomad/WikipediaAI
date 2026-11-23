# Wikipedia AI - Local retrieval system with LLM integration

A structured Python project for processing Wikipedia content using offline 
ZIM archives, local embeddings (Ollama), and vector storage (Qdrant).

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

## Getting Started

### Prerequisites
1. **Python 3.13** (or higher)
2. **Qdrant server** running on `http://127.0.0.1:6333`
3. **Ollama** for embedding generation
4. **ZIM archive** of Wikipedia content (download from https://download.kiwix.org/zim/wikipedia/)

### Installation

```bash
# Clone repository
git clone <repository-url>
cd WikipediaAI

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\\Scripts\\activate
# On Linux/Mac:
source .venv/bin/activate

# Install package in development mode
pip install -e .
```

### Running Tests

```bash
# Run single article test
python test_single_article.py

# Run ingestion tests
python run_ingestion_test.py

# Run comprehensive pipeline test
python test_pipeline_comprehensive.py
```

### Project Structure

```
WikipediaAI/
├── src/
│   └── wikipedia_ai/
│       └── ingestion/      # Main pipeline code
├── test_single_article.py   # Single article test
├── run_ingestion_test.py    # Ingestion test runner
├── test_pipeline_comprehensive.py  # Full pipeline test
└── pyproject.toml           # Project configuration
```

## Development Setup

This project is ready for development and debugging in Visual Studio Code. For detailed setup instructions, see [VS_CODE_SETUP.md](VS_CODE_SETUP.md).

### VS Code Debugging Configuration

To debug the Wikipedia AI pipeline in VS Code:

1. **Open the project in VS Code**
   ```bash
   code .
   ```

2. **Install dependencies** (if not already done):
   ```bash
   # Activate virtual environment
   .venv\\Scripts\\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   
   # Install project in development mode
   pip install -e .
   ```

3. **Debug configurations are available** in the `.vscode/launch.json` file
   - Debug current Python file
   - Debug single article test
   - Debug ingestion tests
   - Debug comprehensive pipeline test

4. **Set breakpoints** and use F5 to start debugging