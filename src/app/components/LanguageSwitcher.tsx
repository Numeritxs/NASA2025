"use client"

import { useState, useEffect, useRef } from "react"
import { useI18n } from "./I18nProvider"

type Locale = "cat" | "gal" | "en" | "es"

export function LanguageSwitcher() {
  const { locale, setLocale, t } = useI18n()
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)
  
  const languages = [
    { code: "cat" as Locale, name: t("language.catalan"), flag: "fi-es-ct" },
    { code: "gal" as Locale, name: t("language.galician"), flag: "fi-es-ga" },
    { code: "es" as Locale, name: t("language.spanish"), flag: "fi-es" },
    { code: "en" as Locale, name: t("language.english"), flag: "fi-us" },
  ]
  
  const currentLanguage = languages.find(l => l.code === locale)
  
  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }
    
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])
  
  return (
    <div className="fixed bottom-4 right-4 z-50">
      {/* Selector de idiomas */}
      <div className="relative" ref={dropdownRef}>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-2 bg-black/60 text-white rounded-lg border border-white/10 px-3 py-2 text-sm hover:bg-black/80 transition-colors"
        >
          <span className={`fi ${currentLanguage?.flag}`}></span>
          <svg 
            className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        
        {isOpen && (
          <div className="absolute bottom-full right-0 mb-2 bg-black/90 text-white rounded-lg border border-white/10 shadow-lg min-w-full">
            {languages.map((lang) => (
              <button
                key={lang.code}
                onClick={() => {
                  setLocale(lang.code)
                  setIsOpen(false)
                }}
                className={`w-full flex items-center gap-2 px-3 py-2 text-sm hover:bg-white/10 transition-colors first:rounded-t-lg last:rounded-b-lg ${
                  locale === lang.code ? 'bg-white/20' : ''
                }`}
              >
                <span className={`fi ${lang.flag}`}></span>
                <span>{lang.name}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
