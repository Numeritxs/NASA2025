// src/app/page.js
"use client"

import { useState } from "react"
import Scene from "./components/scene"

type ModelConfig = {
  path: string
  scale: number
}

const planetModels: Record<string, ModelConfig> = {
  earth: { path: "/models/smaller.glb", scale: 0.5 },
  neptune: { path: "/models/neptune.glb", scale: 0.5 },
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
      alert("Unknown planet. Try earth, neptune, mars.")
    }
  }

  return (
    <div className="w-screen h-screen flex flex-col items-center justify-center bg-black text-white">
      {!planet ? (
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <label>
            Enter planet name:
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="text-black p-2 rounded"
            />
          </label>
          <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded"
          >
            Show Planet
          </button>
        </form>
      ) : (
        <Scene planetModel={planet} sunModel={sunModels["sun"]} />)}
    </div>
  )
}
