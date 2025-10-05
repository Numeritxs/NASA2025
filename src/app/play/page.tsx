"use client"

import { useEffect, useRef } from "react"
import { useI18n } from "../components/I18nProvider"

export default function ShowcasePage() {
  const containerRef = useRef<HTMLDivElement>(null)
  const { t } = useI18n()

  useEffect(() => {
    // Dynamic import to avoid SSR issues
    const loadGame = async () => {
      try {
        // Import the game utilities from main.ts
        const { initializeGame, cleanupGame } = await import("./main")
        
        // Clear container
        if (containerRef.current) {
          containerRef.current.innerHTML = ""
          
          // Initialize the game using the utility function with translation
          initializeGame(containerRef.current, t)
        }
      } catch (error) {
        console.error("Error loading exoplanet game:", error)
        if (containerRef.current) {
          containerRef.current.innerHTML = `
            <div style="padding: 2rem; text-align: center; color: white;">
              <h2>${t("game.error.loading")}</h2>
              <p>${t("game.error.refresh")}</p>
            </div>
          `
        }
      }
    }

    loadGame()

    // Cleanup function
    return () => {
      const cleanup = async () => {
        try {
          const { cleanupGame } = await import("./main")
          cleanupGame()
        } catch (error) {
          console.error("Error during cleanup:", error)
        }
      }
      cleanup()
      
      if (containerRef.current) {
        containerRef.current.innerHTML = ""
      }
    }
  }, [t])

  return (
    <div 
      ref={containerRef}
      style={{
        width: "100vw",
        height: "100vh",
        position: "fixed",
        top: 0,
        left: 0,
        zIndex: 1
      }}
    />
  )
}