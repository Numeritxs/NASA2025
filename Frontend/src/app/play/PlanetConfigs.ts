export interface PlanetConfig {
  textureUrl?: string;
  color?: number;
  atmosphere?: {
    density: number;
    color: number;
  };
  rings?: {
    enabled: boolean;
    color: number;
    opacity: number;
  };
  glow?: {
    enabled: boolean;
    color: number;
    intensity: number;
  };
}

// Planet configurations for different exoplanet types
const planetConfigs: Record<string, PlanetConfig> = {
  'Earth-like': {
    textureUrl: '/textures/earth.jpg',
    color: 0x4a90e2,
    atmosphere: {
      density: 1.0,
      color: 0x87ceeb
    },
    glow: {
      enabled: true,
      color: 0x87ceeb,
      intensity: 0.3
    }
  },
  'Sub Earth': {
    textureUrl: '/textures/earth.jpg',
    color: 0x8b4513,
    atmosphere: {
      density: 0.3,
      color: 0xffa500
    }
  },
  'Super Earth': {
    textureUrl: '/textures/earth.jpg',
    color: 0x228b22,
    atmosphere: {
      density: 1.5,
      color: 0x90ee90
    },
    glow: {
      enabled: true,
      color: 0x90ee90,
      intensity: 0.4
    }
  },
  'Hot Jupiter': {
    textureUrl: '/textures/jupiter.jpg',
    color: 0xff6347,
    atmosphere: {
      density: 5.0,
      color: 0xff4500
    },
    glow: {
      enabled: true,
      color: 0xff4500,
      intensity: 0.8
    }
  },
  'Gas Giant': {
    textureUrl: '/textures/jupiter.jpg',
    color: 0xffa500,
    atmosphere: {
      density: 3.0,
      color: 0xffff00
    },
    rings: {
      enabled: true,
      color: 0xffffff,
      opacity: 0.6
    },
    glow: {
      enabled: true,
      color: 0xffff00,
      intensity: 0.5
    }
  },
  'Ice Giant': {
    textureUrl: '/textures/urano.jpg',
    color: 0x4169e1,
    atmosphere: {
      density: 2.0,
      color: 0x87ceeb
    },
    rings: {
      enabled: true,
      color: 0xffffff,
      opacity: 0.4
    },
    glow: {
      enabled: true,
      color: 0x87ceeb,
      intensity: 0.3
    }
  },
  'Ocean World': {
    textureUrl: '/textures/ocean.jpg',
    color: 0x0066cc,
    atmosphere: {
      density: 1.2,
      color: 0x00bfff
    },
    glow: {
      enabled: true,
      color: 0x00bfff,
      intensity: 0.4
    }
  },
  'Desert World': {
    textureUrl: '/textures/desert.jpg',
    color: 0xcd853f,
    atmosphere: {
      density: 0.5,
      color: 0xffa500
    }
  }
};

/**
 * Get the planet configuration for the top classification
 * @param classifications Array of exoplanet classifications
 * @returns PlanetConfig for the top classification or null if not found
 */
export function getTopClassificationConfig(classifications: Array<{ name: string }>): PlanetConfig | null {
  if (!classifications || classifications.length === 0) {
    return null;
  }
  
  const topClassification = classifications[0];
  return planetConfigs[topClassification.name] || null;
}

/**
 * Get planet configuration by name
 * @param planetName Name of the planet type
 * @returns PlanetConfig or null if not found
 */
export function getPlanetConfig(planetName: string): PlanetConfig | null {
  return planetConfigs[planetName] || null;
}

/**
 * Get all available planet configurations
 * @returns Record of all planet configurations
 */
export function getAllPlanetConfigs(): Record<string, PlanetConfig> {
  return { ...planetConfigs };
}
