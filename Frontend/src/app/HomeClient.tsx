// src/app/HomeClient.tsx

"use client"

import { useRouter } from "next/navigation"
import { useI18n } from "./components/I18nProvider"

export const metadata = {
  title: "Exia",
  description: "Explore planets and play the exoplanet classification game.",
}


export default function Home() {
  const router = useRouter()
  const { t } = useI18n()

  return (
    <div className="w-screen h-screen flex flex-col items-center justify-center bg-gradient-to-b from-black to-gray-900 text-white">
      <h1 className="text-4xl font-bold mb-10">🌌 {t("app.title")}</h1>
      <p className="text-lg mb-8 text-gray-300 text-center max-w-2xl px-4">
        {t("app.description")}
      </p>
      <div className="flex gap-6">
        <button
          onClick={() => router.push("/play")}
          className="px-4 py-2 bg-blue-600 rounded-lg hover:bg-blue-700 shadow-lg text-lg font-semibold"
        >
          🎮 {t("app.start")}
        </button>
      </div>
    </div>
  )
}
