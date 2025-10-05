#!/usr/bin/env python3
"""
Example of how to integrate the backend API with the frontend game
"""
import requests
import json

class ExoplanetAPIClient:
    """Client for interacting with the Exoplanet Prediction API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def classify_exoplanet(self, parameters: dict) -> dict:
        """
        Classify exoplanet parameters and return results compatible with the game.
        
        Args:
            parameters: Dictionary with exoplanet parameters
            
        Returns:
            Dictionary with classification results
        """
        try:
            response = requests.post(
                f"{self.base_url}/classify-exoplanet",
                json=parameters,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"API Error: {response.status_code}",
                    "classifications": [],
                    "similarity": 0.0
                }
                
        except requests.exceptions.ConnectionError:
            return {
                "error": "Cannot connect to API server",
                "classifications": [],
                "similarity": 0.0
            }
        except Exception as e:
            return {
                "error": f"Unexpected error: {str(e)}",
                "classifications": [],
                "similarity": 0.0
            }
    
    def health_check(self) -> bool:
        """Check if the API is healthy and models are loaded."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get("status") == "healthy"
            return False
        except:
            return False

# Example usage for the frontend game
def example_integration():
    """Example of how to use the API client in the game."""
    
    # Initialize the API client
    api_client = ExoplanetAPIClient()
    
    # Check if API is available
    if not api_client.health_check():
        print("❌ API server is not available. Using local classification.")
        return None
    
    # Example exoplanet parameters (from your game)
    exoplanet_params = {
        "koi_prad": 1.5,        # Planet radius (Earth radii)
        "koi_teq": 300,         # Equilibrium temperature (K)
        "koi_period": 365,      # Orbital period (days)
        "koi_model_snr": 8.0,   # Signal-to-noise ratio
        "koi_steff": 5800.0,    # Stellar effective temperature (K)
        "koi_srad": 1.0         # Stellar radius (Solar radii)
    }
    
    # Get classification from API
    result = api_client.classify_exoplanet(exoplanet_params)
    
    if "error" in result:
        print(f"❌ API Error: {result['error']}")
        return None
    
    print("✅ API Classification Result:")
    print(f"Similarity: {result['similarity']:.2%}")
    print("Classifications:")
    for classification in result['classifications']:
        print(f"  - {classification['name']}: {classification['probability']:.2%}")
    
    return result

# Integration with the ExoplanetGame class
def integrate_with_game():
    """
    Example of how to modify the ExoplanetGame.sendToBackend method
    to use this API client.
    """
    
    # In your ExoplanetGame.ts file, you could modify the sendToBackend method:
    
    javascript_code = '''
    // Modified sendToBackend method for ExoplanetGame.ts
    private async sendToBackend(parameters: ExoplanetParameters) {
        try {
            // Convert game parameters to API format
            const apiParams = {
                koi_prad: parameters.radius,
                koi_teq: parameters.temperature,
                koi_period: parameters.orbitalDistance * 365.25, // Convert AU to days (approximate)
                koi_model_snr: parameters.brightness * 10, // Scale brightness to SNR
                koi_steff: 5800.0, // Default stellar temperature
                koi_srad: 1.0 // Default stellar radius
            };
            
            const response = await fetch('http://localhost:8000/classify-exoplanet', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(apiParams)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            // Convert API response to game format
            return {
                classifications: result.classifications,
                similarity: result.similarity
            };
            
        } catch (error) {
            console.error('Backend API error:', error);
            throw error; // Re-throw to trigger fallback to local classification
        }
    }
    '''
    
    print("JavaScript integration code:")
    print(javascript_code)

if __name__ == "__main__":
    print("=== Exoplanet API Integration Example ===\n")
    
    # Run example
    example_integration()
    
    print("\n" + "="*50)
    integrate_with_game()
