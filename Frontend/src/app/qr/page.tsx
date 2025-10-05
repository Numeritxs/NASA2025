// src/app/qr/page.tsx
export const metadata = {
  title: "Exia - QR Code",
  description: "QR code to access the Exia application.",
}

import QRClient from "./QRClient"

export default function QRPage() {
  return <QRClient />
}
