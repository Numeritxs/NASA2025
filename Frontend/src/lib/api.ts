// API client for communicating with the Backend

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ExoplanetData {
  koi_prad?: number;      // Planet radius (Earth radii)
  koi_teq?: number;       // Equilibrium temperature (K)
  koi_period?: number;    // Orbital period (days)
  koi_model_snr?: number; // Signal-to-noise ratio
  koi_steff?: number;     // Stellar effective temperature (K)
  koi_srad?: number;      // Stellar radius (Solar radii)
}

export interface PredictionResponse {
  is_exoplanet?: number;
  is_exoplanet_proba?: number;
  type: string;
  type_top3: Array<[string, number]>;
}

export class ExoplanetAPI {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/health`);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }

  async predictExoplanet(data: ExoplanetData): Promise<PredictionResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Prediction failed:', error);
      throw error;
    }
  }

  async classifyExoplanet(data: ExoplanetData): Promise<PredictionResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/classify-exoplanet`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Classification failed:', error);
      throw error;
    }
  }

  async getModelInfo(): Promise<Record<string, unknown>> {
    try {
      const response = await fetch(`${this.baseUrl}/model-info`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Failed to get model info:', error);
      throw error;
    }
  }
}

// Export a default instance
export const exoplanetAPI = new ExoplanetAPI();
