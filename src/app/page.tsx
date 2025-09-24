// src/app/page.js
"use client"

import { useState } from "react"
import Scene from "./components/scene"

type ModelConfig = {
  path: string
  scale: number
}

const planetModels: Record<string, ModelConfig> = {
  earth: { path: "/models/earth.glb", scale: 0.5 },
  jupiter: { path: "/models/jupiter.glb", scale: 0.2 },
  mars: { path: "/models/mars.glb", scale: 0.5 },
}

const sunModels: Record<string, ModelConfig> = {
  sun: { path: "/models/sun.glb", scale: 1 },
}


export default function Home() {
  const [planet, setPlanet] = useState<ModelConfig | null>(null)
  const [input, setInput] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const key = input.toLowerCase()
    if (planetModels[key]) {
      setPlanet(planetModels[key])
    } else {
      alert("Unknown planet. Try earth, jupiter, mars.")
    }
  }

  const handleReset = () => {
    setPlanet(null)
    setInput("")
  }

  // Conditional background style
  const backgroundStyle = planet
    ? {} // No background when a planet is selected
    : {
      backgroundImage: "url('/images/space-bg.jpg')",
      backgroundSize: "cover",
      backgroundPosition: "center",
    }

  return (
    <div
      className="w-screen h-screen relative text-white"
      style={backgroundStyle}
    >
      {!planet ? (
        <div className="flex items-center justify-center h-full w-full absolute top-0 left-0">
          <div className="bg-black/60 backdrop-blur-md p-8 rounded-xl flex flex-col gap-6 shadow-lg border border-white/20">
            <h2 className="text-2xl font-bold text-white text-center mb-4">Choose Your Planet</h2>
            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
              <label className="flex flex-col text-white font-medium">
                Planet Name:
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="e.g. Earth, Jupiter, Mars"
                  className="mt-1 p-2 rounded-lg text-white placeholder:text-gray-400 bg-black/50 focus:bg-black/70 focus:outline-none focus:ring-2 focus:ring-blue-400"
                />
              </label>
              <button
                type="submit"
                className="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded-lg text-white font-semibold shadow-md hover:shadow-lg transition-all duration-200"
              >
                Show Planet
              </button>
            </form>
          </div>
        </div>
      ) : (
        <Scene planetModel={planet} sunModel={sunModels["sun"]} />
      )}

      {planet && (
        <button
          onClick={handleReset}
          className="absolute top-4 right-4 bg-red-500 hover:bg-red-600 px-4 py-2 rounded text-white z-10"
        >
          Reset
        </button>
      )}
    </div>
  )
}
