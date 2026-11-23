#!/bin/bash

echo "Building Docker containers..."
docker-compose build

echo "Starting containers..."
docker-compose up -d

echo "Waiting for services to start..."
sleep 10

echo "Running tests in Wikipedia AI container..."
docker-compose exec wikipedia-ai pytest --verbose

echo "Checking Qdrant status..."
docker-compose exec qdrant curl -X GET "http://localhost:6333/readyz" -H "accept: application/json"

echo "Checking Ollama status..."
docker-compose exec ollama curl -X GET "http://localhost:11434/api/tags" -H "accept: application/json"

echo "Setup complete! Container logs:"
docker-compose logs wikipedia-ai