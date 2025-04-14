FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a non-root user
RUN useradd -m -s /bin/bash vscode

# Install Python tools using uv
RUN uv pip install --no-cache-dir \
    black \
    pylint \
    mypy \
    pytest

# Set working directory
WORKDIR /workspace

# Switch to non-root user
USER vscode 