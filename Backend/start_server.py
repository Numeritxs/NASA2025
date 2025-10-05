#!/usr/bin/env python3
"""
Startup script for the Exoplanet Prediction API server
"""
import uvicorn
import os
import sys
from pathlib import Path

def check_models():
    """Check if required model files exist."""
    model_dir = Path("modelos")
    required_files = ["clf_exoplanet_type.joblib", "metadata.joblib"]
    optional_files = ["clf_is_exoplanet.joblib"]
    
    print("Checking for model files...")
    
    missing_required = []
    for file in required_files:
        if not (model_dir / file).exists():
            missing_required.append(file)
    
    if missing_required:
        print(f"❌ Missing required model files: {missing_required}")
        print("Please place the trained model files in the 'modelos/' directory:")
        print("  - clf_exoplanet_type.joblib (required)")
        print("  - metadata.joblib (required)")
        print("  - clf_is_exoplanet.joblib (optional)")
        return False
    
    print("✅ Required model files found")
    
    missing_optional = []
    for file in optional_files:
        if not (model_dir / file).exists():
            missing_optional.append(file)
    
    if missing_optional:
        print(f"⚠️  Optional model files missing: {missing_optional}")
        print("Binary classification will be disabled.")
    else:
        print("✅ All model files found")
    
    return True

def main():
    """Main function to start the server."""
    print("🚀 Starting Exoplanet Prediction API Server")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ main.py not found. Please run this script from the Backend directory.")
        sys.exit(1)
    
    # Check for model files
    if not check_models():
        print("\n❌ Cannot start server without required model files.")
        sys.exit(1)
    
    print("\n🌐 Starting server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("🎯 Prediction Endpoint: http://localhost:8000/predict")
    print("🔄 Classification Endpoint: http://localhost:8000/classify-exoplanet")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
