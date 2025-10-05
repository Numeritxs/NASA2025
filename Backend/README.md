# Exoplanet Prediction API

A FastAPI backend for predicting exoplanet types and characteristics using machine learning models.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Place your trained models in the `modelos/` directory:
   - `clf_exoplanet_type.joblib` (required) - Type classifier model
   - `clf_is_exoplanet.joblib` (optional) - Binary exoplanet classifier
   - `metadata.joblib` (required) - Model metadata

3. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /predict
Predict exoplanet type and characteristics.

**Request body:**
```json
{
  "koi_prad": 11.2,
  "koi_teq": 1400,
  "koi_period": 3.5,
  "koi_model_snr": 12.0,
  "koi_steff": 5600.0,
  "koi_srad": 1.0
}
```

**Response:**
```json
{
  "is_exoplanet": 0,
  "is_exoplanet_proba": 0.2898748981614532,
  "type": "gas giant",
  "type_top3": [
    ["gas giant", 0.9654223524775026],
    ["desert world", 0.015313423019318257],
    ["hot jupiter", 0.00822875398741432]
  ]
}
```

### POST /classify-exoplanet
Alternative endpoint compatible with the frontend game.

**Response:**
```json
{
  "classifications": [
    {
      "name": "gas giant",
      "probability": 0.9654223524775026,
      "description": "Exoplanet type: gas giant"
    }
  ],
  "similarity": 0.2898748981614532
}
```

### GET /health
Check API health and model loading status.

### GET /docs
Interactive API documentation (Swagger UI).

## Example Usage

```bash
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
