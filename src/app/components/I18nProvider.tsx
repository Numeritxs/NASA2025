"use client"

import { createContext, useContext, useMemo, useState, ReactNode, useEffect, useRef } from "react"
import cat from "../locales/cat.json"
import gal from "../locales/gal.json"
import en from "../locales/en.json"
import es from "../locales/es.json"

type Locale = "cat" | "gal" | "en" | "es"

type Messages = Record<string, string>

type I18nContextValue = {
  locale: Locale
  setLocale: (l: Locale) => void
  t: (key: string) => string
}

const I18nContext = createContext<I18nContextValue | null>(null)

const LOCALES: Record<Locale, Messages> = { cat, gal, en, es }

export function I18nProvider({ children }: { children: ReactNode }) {
  const [locale, setLocale] = useState<Locale>("en")

  // Use fallback to English if the key is not found in the current locale
  const t = useMemo(() => {
    const messages = LOCALES[locale]
    const fallback = LOCALES["en"]
    return (key: string) => {
      const v = messages[key]
      // If the key is found in the current locale, return the value
      if (v !== undefined && v !== "") return v
      // If the key is not found in the current locale, return the value from the fallback locale
      const fb = fallback[key]
      return fb !== undefined && fb !== "" ? fb : key
    }
  }, [locale])

  const value = useMemo(() => ({ locale, setLocale, t }), [locale, t])

  // Initialize locale from localStorage or browser settings once
  useEffect(() => {
    const saved = (window.localStorage.getItem("locale") as Locale | null)
    if (saved && (saved === "cat" || saved === "gal" || saved === "en" || saved === "es")) {
      setLocale(saved)
      return
    }
    setLocale("en")
  }, [])

  // Persist locale and reflect in <html lang> whenever it changes
  useEffect(() => {
    document.documentElement.lang = locale
    window.localStorage.setItem("locale", locale)
  }, [locale])

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>
}

export function useI18n() {
  const ctx = useContext(I18nContext)
  if (!ctx) throw new Error("useI18n must be used within I18nProvider")
  return ctx
}
