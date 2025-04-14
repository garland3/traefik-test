FROM python:3.12-slim

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app

COPY requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"] 