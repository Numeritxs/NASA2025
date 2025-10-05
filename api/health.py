from http.server import BaseHTTPRequestHandler
import json
import os
import joblib
from pathlib import Path

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Try to load models to check if they're available
            model_dir = os.path.join(os.path.dirname(__file__), "modelos")
            
            # Check if model files exist
            required_files = ["clf_exoplanet_type.joblib", "metadata.joblib"]
            models_loaded = all(os.path.exists(os.path.join(model_dir, f)) for f in required_files)
            
            if models_loaded:
                # Try to actually load the models
                try:
                    joblib.load(os.path.join(model_dir, "clf_exoplanet_type.joblib"))
                    joblib.load(os.path.join(model_dir, "metadata.joblib"))
                    status = "healthy"
                    error = None
                except Exception as e:
                    status = "unhealthy"
                    error = f"Model loading error: {str(e)}"
            else:
                status = "unhealthy"
                error = "Required model files not found"
            
            response = {
                "status": status,
                "models_loaded": models_loaded
            }
            
            if error:
                response["error"] = error
            
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
            self.wfile.write(json.dumps({"status": "error", "error": str(e)}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
