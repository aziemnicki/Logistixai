"use client"

import type React from "react"
import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { SendIcon, Loader2Icon } from "lucide-react"
import { MarkdownRenderer } from "@/components/markdown-renderer"
import { api } from "@/lib/api"

interface ChatMessage {
  id: string
  role: "user" | "assistant"
  content: string
  created_at: string
  sources?: string[]
}

interface ChatSectionProps {
  elementId: string
  elementTitle: string
  elementContent: string
  backgroundData?: string
  reportId: string  // Added reportId for backend API
}

export function ChatSection({ elementId, elementTitle, elementContent, backgroundData, reportId }: ChatSectionProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const suggestedQuestions = [
    `What are the key deadlines and compliance requirements mentioned in "${elementTitle}"?`,
    `How does this impact our current operations and what actions should we prioritize?`,
    `Can you provide more details about the implementation steps and estimated costs?`,
  ]

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = input.trim()
    setInput("")
    setIsLoading(true)

    // Add user message
    const userMsg: ChatMessage = {
      id: `msg-${Date.now()}`,
      role: "user",
      content: userMessage,
      created_at: new Date().toISOString(),
    }
    setMessages((prev) => [...prev, userMsg])

    try {
      // Call backend API with report context
      console.log("🔷 Sending chat message to backend API...")
      const response = await api.sendChatMessage(reportId, userMessage)
      console.log("✅ Received response from backend:", response)

      // Add AI response
      const aiMsg: ChatMessage = {
        id: response.message_id,
        role: "assistant",
        content: response.content,
        created_at: response.created_at,
        sources: response.sources,
      }
      setMessages((prev) => [...prev, aiMsg])
    } catch (error) {
      console.error("❌ Error in chat:", error)
      const errorMsg: ChatMessage = {
        id: `msg-${Date.now()}-error`,
        role: "assistant",
        content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : "Unknown error"}. Please try again.`,
        created_at: new Date().toISOString(),
      }
      setMessages((prev) => [...prev, errorMsg])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSuggestedQuestion = async (question: string) => {
    if (isLoading) return

    setInput("")
    setIsLoading(true)

    // Add user message
    const userMsg: ChatMessage = {
      id: `msg-${Date.now()}`,
      role: "user",
      content: question,
      created_at: new Date().toISOString(),
    }
    setMessages((prev) => [...prev, userMsg])

    try {
      // Call backend API with report context
      console.log("🔷 Sending suggested question to backend API...")
      const response = await api.sendChatMessage(reportId, question)
      console.log("✅ Received response from backend:", response)

      // Add AI response
      const aiMsg: ChatMessage = {
        id: response.message_id,
        role: "assistant",
        content: response.content,
        created_at: response.created_at,
        sources: response.sources,
      }
      setMessages((prev) => [...prev, aiMsg])
    } catch (error) {
      console.error("❌ Error in chat:", error)
      const errorMsg: ChatMessage = {
        id: `msg-${Date.now()}-error`,
        role: "assistant",
        content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : "Unknown error"}. Please try again.`,
        created_at: new Date().toISOString(),
      }
      setMessages((prev) => [...prev, errorMsg])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-4">
      <h3 className="font-semibold text-sm">Ask follow-up 🪄</h3>

      {/* Chat Messages */}
      <div className="space-y-3 max-h-96 overflow-y-auto bg-muted/30 rounded-lg p-4">
        {messages.length === 0 && (
          <div className="space-y-3">
            <p className="text-sm text-muted-foreground text-center">Ask questions about this report element</p>
            <div className="space-y-2">
              {suggestedQuestions.map((question, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestedQuestion(question)}
                  disabled={isLoading}
                  className="w-full text-left p-3 rounded-lg border border-border bg-card hover:bg-accent hover:border-accent-foreground/20 transition-colors text-sm disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-[80%] rounded-lg p-3 ${
                message.role === "user" ? "bg-primary text-primary-foreground" : "bg-card border"
              }`}
            >
              {message.role === "assistant" ? (
                <>
                  <MarkdownRenderer content={message.content} />
                  {message.sources && message.sources.length > 0 && (
                    <div className="mt-2 pt-2 border-t border-border">
                      <p className="text-xs text-muted-foreground mb-1">Sources:</p>
                      <ul className="text-xs space-y-1">
                        {message.sources.map((source, idx) => (
                          <li key={idx} className="text-muted-foreground">• {source}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </>
              ) : (
                <p className="text-sm whitespace-pre-line">{message.content}</p>
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-card border rounded-lg p-3">
              <Loader2Icon className="h-4 w-4 animate-spin" />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Chat Input */}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <Input
          placeholder="Ask a question..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={isLoading}
          className="flex-1"
        />
        <Button type="submit" size="icon" disabled={isLoading || !input.trim()}>
          {isLoading ? <Loader2Icon className="h-4 w-4 animate-spin" /> : <SendIcon className="h-4 w-4" />}
        </Button>
      </form>
    </div>
  )
}
