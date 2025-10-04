"use client"

import { useEffect, useRef } from "react"

export default function ShowcasePage() {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Dynamic import to avoid SSR issues
    const loadGame = async () => {
      try {
        // Import the game utilities from main.ts
        const { initializeGame, cleanupGame } = await import("./main")
        
        // Clear container
        if (containerRef.current) {
          containerRef.current.innerHTML = ""
          
          // Initialize the game using the utility function
          initializeGame(containerRef.current)
        }
      } catch (error) {
        console.error("Error loading exoplanet game:", error)
        if (containerRef.current) {
          containerRef.current.innerHTML = `
            <div style="padding: 2rem; text-align: center; color: white;">
              <h2>Error loading the game</h2>
              <p>Please refresh the page to try again.</p>
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
  }, [])

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