#!/bin/bash

# Test script for Docker setup

echo "🧪 Testing NASA 2025 Docker Setup"
echo "=================================="

# Check if services are running
echo "🔍 Checking if services are running..."
if ! docker compose ps | grep -q "Up"; then
    echo "❌ Services are not running. Please run './start_docker.sh' first."
    exit 1
fi

# Test Backend API
echo "🔍 Testing Backend API..."
BACKEND_URL="http://localhost:8000"

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s "$BACKEND_URL/health" > /dev/null 2>&1; then
        echo "✅ Backend is ready!"
        break
    fi
    echo "⏳ Attempt $i/30 - Backend not ready yet..."
    sleep 2
done

# Test health endpoint
echo "🔍 Testing health endpoint..."
if curl -s "$BACKEND_URL/health" | grep -q "healthy"; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    echo "Backend logs:"
    docker compose logs backend --tail=10
    exit 1
fi

# Test prediction endpoint
echo "🔍 Testing prediction endpoint..."
PREDICTION_RESPONSE=$(curl -s -X POST "$BACKEND_URL/predict" \
    -H "Content-Type: application/json" \
    -d '{
        "koi_prad": 1.0,
        "koi_teq": 300.0,
        "koi_period": 365.0,
        "koi_model_snr": 10.0,
        "koi_steff": 5000.0,
        "koi_srad": 1.0
    }')

if echo "$PREDICTION_RESPONSE" | grep -q "type"; then
    echo "✅ Prediction endpoint working"
    echo "📊 Sample prediction: $PREDICTION_RESPONSE"
else
    echo "❌ Prediction endpoint failed"
    echo "Response: $PREDICTION_RESPONSE"
fi

# Test Frontend
echo "🔍 Testing Frontend..."
FRONTEND_URL="http://localhost:3000"

# Wait for frontend to be ready
echo "⏳ Waiting for frontend to be ready..."
for i in {1..30}; do
    if curl -s "$FRONTEND_URL" > /dev/null 2>&1; then
        echo "✅ Frontend is ready!"
        break
    fi
    echo "⏳ Attempt $i/30 - Frontend not ready yet..."
    sleep 2
done

# Test frontend response
if curl -s "$FRONTEND_URL" | grep -q "html"; then
    echo "✅ Frontend is serving content"
else
    echo "❌ Frontend not responding properly"
    echo "Frontend logs:"
    docker compose logs frontend --tail=10
fi

echo ""
echo "🎉 Docker setup test completed!"
echo "🌐 Frontend: $FRONTEND_URL"
echo "🔧 Backend: $BACKEND_URL"
echo "📚 API Docs: $BACKEND_URL/docs"
