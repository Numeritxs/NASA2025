// src/app/qr/QRClient.tsx

"use client"

import { useEffect, useState } from "react"
import { useI18n } from "../components/I18nProvider"
import QRCode from "qrcode"

export default function QRClient() {
  const { t } = useI18n()
  const [qrCodeUrl, setQrCodeUrl] = useState<string>("")
  const [ipAddress] = useState<string>("10.19.229.83") // IP obtenida del sistema
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const generateQR = async () => {
      try {
        const url = `http://${ipAddress}:3000`
        const qrCodeDataUrl = await QRCode.toDataURL(url, {
          width: 256,
          margin: 2,
          color: {
            dark: '#000000',
            light: '#FFFFFF'
          }
        })
        setQrCodeUrl(qrCodeDataUrl)
        setIsLoading(false)
      } catch (error) {
        console.error('Error generating QR code:', error)
        setIsLoading(false)
      }
    }

    generateQR()
  }, [ipAddress])

  return (
    <div className="w-screen h-screen flex flex-col items-center justify-center bg-gradient-to-b from-black to-gray-900 text-white">
      <h1 className="text-4xl font-bold mb-10">🌌 {t("app.title")}</h1>
      <p className="text-lg mb-8 text-gray-300 text-center max-w-2xl px-4">
        {t("app.description")}
      </p>
      
      <div className="flex flex-col items-center gap-6">
        {isLoading ? (
          <div className="w-64 h-64 flex items-center justify-center bg-gray-800 rounded-lg">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-4">
            <div className="w-64 h-64 flex items-center justify-center bg-white rounded-lg p-4">
              {qrCodeUrl && (
                <img 
                  src={qrCodeUrl} 
                  alt="QR Code" 
                  className="w-full h-full"
                />
              )}
            </div>
            <p className="text-sm text-gray-400 text-center">
              {t("qr.scan")}
            </p>
            <p className="text-xs text-gray-500 text-center font-mono">
              {t("qr.url").replace("{ip}", ipAddress)}
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
