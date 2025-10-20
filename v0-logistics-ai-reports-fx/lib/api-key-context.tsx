"use client"

import React, { createContext, useContext, useState, useEffect, type ReactNode } from "react"

interface APIKeyContextType {
  apiKey: string | null
  setApiKey: (key: string | null) => void
  hasApiKey: boolean
}

const APIKeyContext = createContext<APIKeyContextType | undefined>(undefined)

export function APIKeyProvider({ children }: { children: ReactNode }) {
  const [apiKey, setApiKeyState] = useState<string | null>(null)

  // Load API key from sessionStorage on mount (only in browser)
  useEffect(() => {
    if (typeof window !== "undefined") {
      const storedKey = sessionStorage.getItem("anthropic_api_key")
      if (storedKey) {
        setApiKeyState(storedKey)
      }
    }
  }, [])

  const setApiKey = (key: string | null) => {
    setApiKeyState(key)
    if (typeof window !== "undefined") {
      if (key) {
        sessionStorage.setItem("anthropic_api_key", key)
      } else {
        sessionStorage.removeItem("anthropic_api_key")
      }
    }
  }

  return (
    <APIKeyContext.Provider value={{ apiKey, setApiKey, hasApiKey: !!apiKey }}>
      {children}
    </APIKeyContext.Provider>
  )
}

export function useAPIKey() {
  const context = useContext(APIKeyContext)
  if (context === undefined) {
    throw new Error("useAPIKey must be used within an APIKeyProvider")
  }
  return context
}
