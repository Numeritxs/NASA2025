// src/app/page.tsx
export const metadata = {
  title: "Exia",
  description: "Choose between exploring planets or running AI classifications.",
}

import HomeClient from "./HomeClient"

export default function HomePage() {
  return <HomeClient />
}
