"use client"

import { useState } from "react"
import { useAPIKey } from "@/lib/api-key-context"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { AlertCircle, Key, X } from "lucide-react"

export function APIKeyBanner() {
  const { apiKey, setApiKey, hasApiKey } = useAPIKey()
  const [inputValue, setInputValue] = useState("")
  const [showInput, setShowInput] = useState(!hasApiKey)
  const [error, setError] = useState("")

  const handleSaveKey = () => {
    const trimmedKey = inputValue.trim()

    // Validate key format
    if (!trimmedKey) {
      setError("Please enter an API key")
      return
    }

    if (!trimmedKey.startsWith("sk-ant-")) {
      setError("Invalid API key format. Anthropic API keys should start with 'sk-ant-'")
      return
    }

    // Key is valid
    setApiKey(trimmedKey)
    setInputValue("")
    setShowInput(false)
    setError("")
  }

  if (hasApiKey && !showInput) {
    return (
      <Card className="mb-6 border-green-500/50 bg-green-50 dark:bg-green-950/20">
        <CardContent className="flex items-center justify-between p-4">
          <div className="flex items-center gap-3">
            <Key className="h-5 w-5 text-green-600 dark:text-green-400" />
            <div>
              <p className="text-sm font-medium text-green-900 dark:text-green-100">
                API Key Connected
              </p>
              <p className="text-xs text-green-700 dark:text-green-300">
                Your Anthropic API key is active and ready to use.
              </p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowInput(true)}
              className="border-green-600 text-green-600 hover:bg-green-100 dark:border-green-400 dark:text-green-400 dark:hover:bg-green-950"
            >
              Change Key
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => {
                setApiKey(null)
                setShowInput(true)
              }}
              className="text-green-600 hover:bg-green-100 hover:text-green-700 dark:text-green-400 dark:hover:bg-green-950"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="mb-6 border-amber-500/50 bg-amber-50 dark:bg-amber-950/20">
      <CardContent className="p-4">
        <div className="flex items-start gap-3">
          <AlertCircle className="h-5 w-5 text-amber-600 dark:text-amber-400 mt-0.5" />
          <div className="flex-1">
            <p className="text-sm font-medium text-amber-900 dark:text-amber-100 mb-1">
              API Key Required
            </p>
            <p className="text-xs text-amber-700 dark:text-amber-300 mb-3">
              To use this application, you'll need your own Anthropic API key. Your key is stored securely in your
              browser session only and is never sent to our servers.{" "}
              <a
                href="https://console.anthropic.com/"
                target="_blank"
                rel="noopener noreferrer"
                className="font-medium underline hover:text-amber-800 dark:hover:text-amber-200"
              >
                Get your API key here →
              </a>
            </p>
            <div className="flex flex-col gap-2">
              <div className="flex gap-2">
                <Input
                  type="password"
                  placeholder="sk-ant-api03-..."
                  value={inputValue}
                  onChange={(e) => {
                    setInputValue(e.target.value)
                    setError("") // Clear error when user types
                  }}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      handleSaveKey()
                    }
                  }}
                  className="max-w-md border-amber-300 bg-white dark:border-amber-700 dark:bg-amber-950/50"
                />
                <Button
                  onClick={handleSaveKey}
                  disabled={!inputValue.trim()}
                  className="bg-amber-600 text-white hover:bg-amber-700 dark:bg-amber-700 dark:hover:bg-amber-600"
                >
                  Save Key
                </Button>
              </div>
              {error && (
                <p className="text-xs text-red-600 dark:text-red-400">
                  {error}
                </p>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
