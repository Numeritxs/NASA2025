#!/bin/bash

echo "🧪 Testing simple prediction in Docker..."

# Build the Docker image
docker build -t exoplanet-api .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    
    echo "🔮 Running simple prediction test..."
    
    # Run the simple prediction script
    docker run --rm -v $(pwd)/modelos:/app/modelos exoplanet-api python simple_prediction.py
    
else
    echo "❌ Failed to build Docker image"
    exit 1
fi
