FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv and add to PATH
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    echo 'export PATH="/root/.cargo/bin:$PATH"' >> /root/.bashrc && \
    echo 'export PATH="/root/.cargo/bin:$PATH"' >> /etc/profile

# Create a non-root user
RUN useradd -m -s /bin/bash vscode && \
    mkdir -p /home/vscode/.cargo/bin && \
    chown -R vscode:vscode /home/vscode

# Copy uv to vscode user's PATH
RUN cp /root/.cargo/bin/uv /home/vscode/.cargo/bin/ && \
    chown vscode:vscode /home/vscode/.cargo/bin/uv

# Set environment variables for vscode user
USER vscode
ENV PATH="/home/vscode/.cargo/bin:${PATH}"

# Install Python tools using uv
RUN uv pip install --no-cache-dir \
    black \
    pylint \
    mypy \
    pytest

# Set working directory
WORKDIR /workspace 