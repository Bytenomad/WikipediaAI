#!/bin/bash

# Create a simple test environment for Open WebUI
echo "Creating test environment..."

# Ensure we have the necessary directories
mkdir -p ./open-webui/vector_db
mkdir -p ./open-webui/uploads

# Copy the secret key if it exists
if [ -f "./open-webui/.webui_secret_key" ]; then
    echo "Secret key found"
else
    # Generate a simple secret key for testing
    echo "Generating new secret key..."
    openssl rand -hex 32 > ./open-webui/.webui_secret_key
fi

# Run Open WebUI with minimal configuration
echo "Starting Open WebUI with minimal config..."
docker run --rm \
  -p 8081:8080 \
  -v $(pwd)/open-webui/vector_db:/app/vector_db \
  -v $(pwd)/open-webui/uploads:/app/uploads \
  -v $(pwd)/open-webui/.webui_secret_key:/app/.webui_secret_key \
  -e DATABASE_URL=sqlite:////app/vector_db/chroma.sqlite3 \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -e WEBUI_NAME=WikiAI \
  -e WEBUI_SECRET_KEY_FILE=/app/.webui_secret_key \
  -e INIT_DB=true \
  -e WEBUI_DEBUG=true \
  --name test-openwebui ghcr.io/open-webui/open-webui:main