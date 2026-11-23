FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libzim-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir setuptools wheel
RUN pip install --no-cache-dir -e .

# Copy source code
COPY src/ ./src/
COPY wikipedia/ ./wikipedia/

# Copy test files for verification
COPY tests/ ./tests/

# Expose ports if needed (for web UI)
EXPOSE 8080

# Default command - no-op to keep container running
CMD ["tail", "-f", "/dev/null"]