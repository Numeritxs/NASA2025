// Mapeo de nombres de planetas a claves de traducción
export const PLANET_TRANSLATION_KEYS: Record<string, { name: string; desc: string }> = {
  'Earth-like': {
    name: 'planet.earth-like',
    desc: 'planet.earth-like.desc'
  },
  'Super Earth': {
    name: 'planet.super-earth',
    desc: 'planet.super-earth.desc'
  },
  'Ocean World': {
    name: 'planet.ocean-world',
    desc: 'planet.ocean-world.desc'
  },
  'Hot Jupiter': {
    name: 'planet.hot-jupiter',
    desc: 'planet.hot-jupiter.desc'
  },
  'Gas Giant': {
    name: 'planet.gas-giant',
    desc: 'planet.gas-giant.desc'
  },
  'Ice Giant': {
    name: 'planet.ice-giant',
    desc: 'planet.ice-giant.desc'
  },
  'Desert World': {
    name: 'planet.desert-world',
    desc: 'planet.desert-world.desc'
  }
};

// Obtains the translation of a planet
export function getPlanetTranslation(planetName: string, translationKey: 'name' | 'desc'): string {
  const keys = PLANET_TRANSLATION_KEYS[planetName];
  if (!keys) {
    console.warn(`No translation keys found for planet: ${planetName}`);
    return planetName; // Fallback to the original name
  }
  return keys[translationKey];
}
