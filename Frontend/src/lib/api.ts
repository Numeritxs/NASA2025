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

export interface ClassificationResult {
  name: string;
  probability: number;
  description: string;
}

export interface ConvertedPredictionResponse {
  classifications: ClassificationResult[];
  similarity: number;
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

  async classifyExoplanet(data: ExoplanetData): Promise<ConvertedPredictionResponse> {
    try {
      console.log('API: Making request to', `${this.baseUrl}/predict`);
      console.log('API: Request data', data);
      
      const response = await fetch(`${this.baseUrl}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      console.log('API: Response status', response.status);
      console.log('API: Response headers', Object.fromEntries(response.headers.entries()));

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log('API: Response data', result);
      
      // Convert the /predict response format to the expected format
      const classifications = [];
      if (result.type_top3) {
        for (const [spanishName, probability] of result.type_top3) {
          const englishName = this.mapSpanishToEnglishName(spanishName);
          classifications.push({
            name: englishName,
            probability: probability,
            description: `Exoplanet type: ${englishName}`
          });
        }
      }
      
      return {
        classifications: classifications,
        similarity: result.is_exoplanet_proba || 0.0
      };
    } catch (error) {
      console.error('Classification failed:', error);
      throw error;
    }
  }

  // Map Spanish backend names to English frontend names
  private mapSpanishToEnglishName(spanishName: string): string {
    const nameMap: Record<string, string> = {
      // Basic types
      'subterrestre': 'Sub Earth',
      'subterrestre_caliente': 'Desert World', // Hot subterrestrial -> Desert World
      'terraneo': 'Earth-like', 
      'terraneo_caliente': 'Desert World', // Hot terrestrial -> Desert World
      'super_tierra': 'Super Earth',
      'super_tierra_caliente': 'Desert World', // Hot super earth -> Desert World
      'mini_neptuno': 'Ice Giant',
      'mini_neptuno_caliente': 'Hot Jupiter', // Hot mini neptune -> Hot Jupiter
      'neptuniano': 'Ice Giant',
      'neptuniano_caliente': 'Hot Jupiter', // Hot neptunian -> Hot Jupiter
      'joviano': 'Gas Giant',
      'joviano_caliente': 'Hot Jupiter'
    };
    
    console.log(`API: Mapping "${spanishName}" to "${nameMap[spanishName] || spanishName}"`);
    return nameMap[spanishName] || spanishName; // Return original if no mapping found
  }

  // Convert frontend parameters to backend format
  convertGameParametersToBackend(parameters: any): ExoplanetData {
    console.log('API: Converting frontend parameters:', parameters);
    
    // Calculate orbital period from orbital distance using Kepler's laws
    // P = sqrt(a^3) for a in AU, P in years, then convert to days
    const orbitalPeriodDays = Math.sqrt(Math.pow(parameters.orbitalDistance, 3)) * 365.25;
    
    // Estimate stellar properties from brightness and mass
    // Brightness can be used to estimate stellar temperature
    const stellarTemp = Math.max(3000, 3000 + (parameters.brightness - 0.1) * 2000);
    
    // Estimate stellar radius from mass (simplified relation)
    const stellarRadius = Math.max(0.1, Math.min(10, parameters.mass * 0.5 + 0.5));
    
    // Calculate signal-to-noise ratio based on planet properties
    // Higher mass and radius planets have better SNR
    const modelSnr = Math.max(1.0, Math.min(50.0, (parameters.mass * parameters.radius * parameters.brightness) * 5));

    const backendData = {
      koi_prad: parameters.radius,           // Planet radius in Earth radii
      koi_teq: parameters.temperature,       // Equilibrium temperature in K
      koi_period: orbitalPeriodDays,         // Orbital period in days
      koi_model_snr: modelSnr,               // Signal-to-noise ratio
      koi_steff: stellarTemp,                // Stellar effective temperature in K
      koi_srad: stellarRadius                // Stellar radius in Solar radii
    };
    
    console.log('API: Converted to backend format:', backendData);
    return backendData;
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
