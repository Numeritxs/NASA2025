// src/app/HomeClient.tsx

"use client"

import { useRouter } from "next/navigation"

export const metadata = {
  title: "Exia",
  description: "Explore planets and play the exoplanet classification game.",
}


export default function Home() {
  const router = useRouter()

  return (
    <div className="w-screen h-screen flex flex-col items-center justify-center bg-gradient-to-b from-black to-gray-900 text-white">
      <h1 className="text-4xl font-bold mb-10">🌌 Welcome to Exia</h1>
      <div className="flex gap-6">
        <button
          onClick={() => router.push("/play")}
          className="px-4 py-2 bg-blue-600 rounded-lg hover:bg-blue-700 shadow-lg text-lg font-semibold"
        >
          🎮 Start
        </button>
      </div>
    </div>
  )
}
