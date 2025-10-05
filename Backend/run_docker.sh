#!/bin/bash

echo "🐳 Building Exoplanet Prediction API Docker container..."

# Build the Docker image
docker build -t exoplanet-api .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    
    echo "🚀 Starting the API server..."
    echo "📖 API will be available at: http://localhost:8000"
    echo "📚 Documentation at: http://localhost:8000/docs"
    echo "🔍 Health check at: http://localhost:8000/health"
    echo ""
    echo "Press Ctrl+C to stop the server"
    
    # Run the container
    docker run -p 8000:8000 -v $(pwd)/modelos:/app/modelos exoplanet-api
    
else
    echo "❌ Failed to build Docker image"
    exit 1
fi
