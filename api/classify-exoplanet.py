from http.server import BaseHTTPRequestHandler
import json
import os
import numpy as np
import pandas as pd
import joblib
from typing import Dict, List, Tuple, Optional

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Parse request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Make prediction
            result = self.predict_exoplanet(data)
            
            # Format response for frontend compatibility
            classifications = []
            for type_name, probability in result["type_top3"]:
                classifications.append({
                    "name": type_name,
                    "probability": probability,
                    "description": f"Exoplanet type: {type_name}"
                })
            
            response = {
                "classifications": classifications,
                "similarity": result.get("is_exoplanet_proba", 0.0)
            }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def predict_exoplanet(self, example: Dict) -> Dict:
        """
        Predict exoplanet characteristics from input data.
        
        Args:
            example: Dictionary containing exoplanet parameters
            
        Returns:
            Dictionary with prediction results
        """
        try:
            model_dir = os.path.join(os.path.dirname(__file__), "modelos")
            
            # Load models
            clf_bin = None
            clf_type = None
            meta = None
            
            # Load binary classifier if it exists
            p_bin = os.path.join(model_dir, "clf_is_exoplanet.joblib")
            if os.path.exists(p_bin):
                clf_bin = joblib.load(p_bin)
                
            # Load type classifier (required)
            clf_type = joblib.load(os.path.join(model_dir, "clf_exoplanet_type.joblib"))
            
            # Load metadata (required)
            meta = joblib.load(os.path.join(model_dir, "metadata.joblib"))
            
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
            raise Exception(f"Error making prediction: {str(e)}")
