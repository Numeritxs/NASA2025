from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Tuple, Optional
import os
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
import os
from typing import Optional, Tuple
import joblib


app = FastAPI(
    title="Exoplanet Prediction API",
    description="API for predicting exoplanet types and characteristics using machine learning models",
    version="1.0.0"
)

# Request model for exoplanet data
class ExoplanetData(BaseModel):
    koi_prad: Optional[float] = None      # Planet radius (Earth radii)
    koi_teq: Optional[float] = None       # Equilibrium temperature (K)
    koi_period: Optional[float] = None    # Orbital period (days)
    koi_model_snr: Optional[float] = None # Signal-to-noise ratio
    koi_steff: Optional[float] = None     # Stellar effective temperature (K)
    koi_srad: Optional[float] = None      # Stellar radius (Solar radii)

# Response model for predictions
class PredictionResponse(BaseModel):
    is_exoplanet: Optional[int] = None
    is_exoplanet_proba: Optional[float] = None
    type: str
    type_top3: List[Tuple[str, float]]

# Global variables to store loaded models
clf_bin = None
clf_type = None
meta = None

def load_models(model_dir: str = "modelos") -> Tuple[Optional[object], object, dict]:
    """
    Load the trained models and metadata.
    
    Args:
        model_dir: Directory containing the model files
        
    Returns:
        Tuple of (binary classifier, type classifier, metadata)
    """
    global clf_bin, clf_type, meta
    
    if clf_bin is not None and clf_type is not None and meta is not None:
        return clf_bin, clf_type, meta
    
    try:
        # Load binary classifier if it exists
        p_bin = os.path.join(model_dir, "clf_is_exoplanet.joblib")
        if os.path.exists(p_bin):
            clf_bin = joblib.load(p_bin)
        else:
            clf_bin = None
            
        # Load type classifier (required)
        clf_type = joblib.load(os.path.join(model_dir, "clf_exoplanet_type.joblib"))
        
        # Load metadata (required)
        meta = joblib.load(os.path.join(model_dir, "metadata.joblib"))
        
        return clf_bin, clf_type, meta
        
    except Exception as e:
        print(f"Error loading models: {str(e)}")  # Debug print
        raise HTTPException(
            status_code=500,
            detail=f"Error loading models: {str(e)}"
        )

def predict_exoplanet(example: Dict, model_dir: str = "modelos") -> Dict:
    """
    Predict exoplanet characteristics from input data.
    
    Args:
        example: Dictionary containing exoplanet parameters
        model_dir: Directory containing the model files
        
    Returns:
        Dictionary with prediction results
    """
    try:
        clf_bin, clf_type, meta = load_models(model_dir)
        
        # Get required columns from metadata
        cols = meta["num_cols"] + meta["cat_cols"]
        
        # Create DataFrame with the input data
        X = pd.DataFrame([{c: example.get(c, np.nan) for c in cols}])
        
        out = {}
        
        # Binary classification (if model exists)
        if clf_bin is not None:
            proba = clf_bin.predict_proba(X)[0, 1]
            out["is_exoplanet"] = int(proba >= 0.5)
            out["is_exoplanet_proba"] = float(proba)
        
        # Type classification
        proba_type = clf_type.predict_proba(X)[0]
        pred_type = clf_type.predict(X)[0]
        classes = clf_type.named_steps["clf"].classes_
        
        # Get top 3 predictions
        topk = np.argsort(proba_type)[::-1][:3]
        out["type"] = str(pred_type)
        out["type_top3"] = [(str(classes[i]), float(proba_type[i])) for i in topk]
        
        return out
        
    except Exception as e:
        print(f"Error making prediction: {str(e)}")  # Debug print
        raise HTTPException(
            status_code=500,
            detail=f"Error making prediction: {str(e)}"
        )

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Exoplanet Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "/predict": "POST - Make exoplanet predictions",
            "/health": "GET - Check API health",
            "/docs": "GET - API documentation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Try to load models to check if they're available
        load_models()
        return {"status": "healthy", "models_loaded": True}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/test")
async def test_endpoint():
    """Simple test endpoint that doesn't require models."""
    return {
        "message": "API is working!",
        "server_time": "2024-01-01T00:00:00Z",
        "endpoints_available": [
            "/",
            "/health", 
            "/test",
            "/docs",
            "/predict (requires models)",
            "/classify-exoplanet (requires models)"
        ]
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(exoplanet_data: ExoplanetData):
    """
    Predict exoplanet type and characteristics.
    
    Args:
        exoplanet_data: Exoplanet parameters (radius, temperature, etc.)
        
    Returns:
        Prediction results including type and probabilities
    """
    try:
        # Convert Pydantic model to dict
        example = exoplanet_data.dict()
        
        # Remove None values and convert to appropriate types
        example = {k: v for k, v in example.items() if v is not None}
        
        if not example:
            raise HTTPException(
                status_code=400,
                detail="At least one parameter must be provided"
            )
        
        # Make prediction
        result = predict_exoplanet(example)
        
        return PredictionResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/classify-exoplanet")
async def classify_exoplanet(exoplanet_data: ExoplanetData):
    """
    Alternative endpoint for exoplanet classification (compatible with frontend).
    
    Args:
        exoplanet_data: Exoplanet parameters
        
    Returns:
        Classification results with similarity score
    """
    try:
        # Convert Pydantic model to dict
        example = exoplanet_data.dict()
        
        # Remove None values
        example = {k: v for k, v in example.items() if v is not None}
        
        if not example:
            raise HTTPException(
                status_code=400,
                detail="At least one parameter must be provided"
            )
        
        # Make prediction
        result = predict_exoplanet(example)
        
        # Format response for frontend compatibility
        classifications = []
        for type_name, probability in result["type_top3"]:
            classifications.append({
                "name": type_name,
                "probability": probability,
                "description": f"Exoplanet type: {type_name}"
            })
        
        return {
            "classifications": classifications,
            "similarity": result.get("is_exoplanet_proba", 0.0)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
