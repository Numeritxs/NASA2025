# Exoplanet Prediction API - Docker Setup

This setup uses Docker to ensure consistent environment and package versions for the exoplanet prediction API.

## Quick Start

### Option 1: Run the API Server
```bash
./run_docker.sh
```
This will:
- Build the Docker image
- Start the FastAPI server on http://localhost:8000
- Mount the modelos directory for model access

### Option 2: Test Simple Prediction
```bash
./test_docker_prediction.sh
```
This will:
- Build the Docker image
- Run the simple prediction script to test if models work

### Option 3: Using Docker Compose
```bash
# Run the API server
docker-compose up exoplanet-api

# Test simple prediction
docker-compose --profile test up simple-prediction
```

## Manual Docker Commands

### Build the image:
```bash
docker build -t exoplanet-api .
```

### Run the API server:
```bash
docker run -p 8000:8000 -v $(pwd)/modelos:/app/modelos exoplanet-api
```

### Run simple prediction test:
```bash
docker run --rm -v $(pwd)/modelos:/app/modelos exoplanet-api python simple_prediction.py
```

## API Endpoints

Once running, the API will be available at:

- **Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs
- **Predict**: http://localhost:8000/predict (POST)
- **Classify**: http://localhost:8000/classify-exoplanet (POST)

## Test the API

```bash
# Health check
curl http://localhost:8000/health

# Make a prediction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "koi_prad": 11.2,
    "koi_teq": 1400,
    "koi_period": 3.5,
    "koi_model_snr": 12.0,
    "koi_steff": 5600.0,
    "koi_srad": 1.0
  }'
```

## Troubleshooting

If you get permission errors, make sure the scripts are executable:
```bash
chmod +x run_docker.sh test_docker_prediction.sh
```

If models are not found, ensure the `modelos/` directory contains:
- `clf_exoplanet_type.joblib`
- `metadata.joblib`
- `clf_is_exoplanet.joblib` (optional)
