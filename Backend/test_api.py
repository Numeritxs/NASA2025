#!/usr/bin/env python3
"""
Test script for the Exoplanet Prediction API
"""
import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_predict():
    """Test the prediction endpoint."""
    print("Testing prediction endpoint...")
    
    # Example data from the notebook
    test_data = {
        "koi_prad": 11.2,
        "koi_teq": 1400,
        "koi_period": 3.5,
        "koi_model_snr": 12.0,
        "koi_steff": 5600.0,
        "koi_srad": 1.0
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("Prediction Result:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the server is running.")
    print()

def test_classify():
    """Test the classification endpoint."""
    print("Testing classification endpoint...")
    
    test_data = {
        "koi_prad": 11.2,
        "koi_teq": 1400,
        "koi_period": 3.5,
        "koi_model_snr": 12.0,
        "koi_steff": 5600.0,
        "koi_srad": 1.0
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/classify-exoplanet",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("Classification Result:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the server is running.")
    print()

if __name__ == "__main__":
    print("=== Exoplanet Prediction API Tests ===\n")
    
    test_health()
    test_predict()
    test_classify()
    
    print("Tests completed!")
    print("\nTo run the API server:")
    print("cd /home/luis/proyects/NASA2025/Backend")
    print("python main.py")
