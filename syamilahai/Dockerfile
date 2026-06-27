FROM python:3.11-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire syamilahai directory contents
COPY . .

# Expose port for FastAPI
EXPOSE 8001

# Run uvicorn server
CMD ["uvicorn", "5_api_mufti:app", "--host", "0.0.0.0", "--port", "8001"]
