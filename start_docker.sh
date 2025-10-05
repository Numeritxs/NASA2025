#!/bin/bash

# NASA 2025 Exoplanet Application Docker Startup Script

echo "🚀 Starting NASA 2025 Exoplanet Application"
echo "============================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found. Please run this script from the project root."
    exit 1
fi

# Stop any existing services
echo "🛑 Stopping any existing services..."
docker compose down

# Start the services
echo "🚀 Starting services with Docker Compose..."
docker compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 15

# Check if services are running
echo "🔍 Checking service status..."
docker compose ps

echo ""
echo "✅ Application is starting up!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "To view logs: docker compose logs -f"
echo "To stop: docker compose down"
echo "============================================="
