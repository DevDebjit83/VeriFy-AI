FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libsndfile1 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_ai.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_ai.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=90s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health', timeout=5)" || exit 1

# Run the application
CMD exec uvicorn ai_server_sota:app --host 0.0.0.0 --port ${PORT}
