#!/bin/bash

# Initialize database permissions for Open WebUI
echo "Initializing database permissions..."

# Create directories if they don't exist
mkdir -p /app/vector_db
mkdir -p /app/uploads

# Set proper ownership and permissions
chown -R root:root /app/vector_db
chmod -R 755 /app/vector_db
chown -R root:root /app/uploads
chmod -R 755 /app/uploads

# Ensure the secret key file has proper permissions
chmod 600 /app/.webui_secret_key

echo "Database initialization complete."