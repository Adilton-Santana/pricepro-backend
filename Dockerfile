# Use Python 3.11 slim base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set Python to unbuffered mode (logs aparecem imediatamente)
ENV PYTHONUNBUFFERED=1

# Expose port (Railway will override with $PORT)
EXPOSE 8000

# Run the application using uvicorn with PORT variable expansion + logging
CMD sh -c "echo '🔍 DEBUG: Valor da variável PORT = ${PORT}' && \
           echo '🚀 Iniciando uvicorn na porta ${PORT:-8000}...' && \
           echo '📍 Host: 0.0.0.0' && \
           echo '🔍 Testando imports...' && \
           python -c 'from main import app; print(\"✅ FastAPI app importada com sucesso!\")' && \
           echo '▶️  Iniciando servidor...' && \
           uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --log-level info"
