# Use Python 3.10 as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create modelos directory if it doesn't exist
RUN mkdir -p modelos

# Expose port 8000
EXPOSE 8000

# Default command to run the FastAPI server
CMD ["python", "start_server.py"]

# Alternative: Run simple prediction script
# CMD ["python", "simple_prediction.py"]
