import { ExoplanetGame } from './ExoplanetGame';
import type { ExoplanetGame as ExoplanetGameType, GameState } from './ExoplanetGame';

/**
 * Utility functions for managing the Exoplanet Game
 */

let gameInstance: ExoplanetGameType | null = null;

/**
 * Initialize the Exoplanet Game in a container
 */
export function initializeGame(container: HTMLElement): ExoplanetGameType {
  if (gameInstance) {
    gameInstance = null; // Clean up previous instance
  }
  
  gameInstance = new ExoplanetGame(container);
  return gameInstance;
}

/**
 * Get the current game instance
 */
export function getGameInstance(): ExoplanetGameType | null {
  return gameInstance;
}

/**
 * Get current game state
 */
export function getGameState(): GameState | null {
  return gameInstance?.getGameState() || null;
}

/**
 * Restart the current game
 */
export function restartGame(): void {
  if (gameInstance) {
    // Access private method through any type casting
    (gameInstance as any).restartGame();
  }
}

/**
 * Clean up the game instance
 */
export function cleanupGame(): void {
  gameInstance = null;
}

// Legacy initialization for direct script usage
export function initializeLegacyGame(): ExoplanetGameType {
  return initializeGame(document.body);
}

