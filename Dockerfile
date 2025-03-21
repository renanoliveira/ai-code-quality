# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install git for commit creation
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -e ".[dev]"

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command
ENTRYPOINT ["ai-quality-ci"]
