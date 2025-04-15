FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -s /bin/bash appuser && \
    chown -R appuser:appuser /home/appuser

# Set working directory and ensure proper permissions
WORKDIR /app
RUN chown -R appuser:appuser /app

# Switch to appuser
USER appuser

# Create and activate virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install uv and project dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir uv
RUN python -m uv pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"] 