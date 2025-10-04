// src/app/page.tsx
export const metadata = {
  title: "Exia",
  description: "Explore planets and play the exoplanet classification game.",
}

import HomeClient from "./HomeClient"

export default function HomePage() {
  return <HomeClient />
}
