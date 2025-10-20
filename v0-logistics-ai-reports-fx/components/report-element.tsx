"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  MessageSquareIcon,
  MessageCircleIcon,
  ExternalLinkIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  TruckIcon,
  TrendingDownIcon,
} from "lucide-react"
import { VotingSection } from "@/components/voting-section"
import { CommentsSection } from "@/components/comments-section"
import { ChatSection } from "@/components/chat-section"
import Image from "next/image"

interface Source {
  title: string
  url: string
}

interface Element {
  id: string
  title: string
  content: string
  category?: string
  summary?: string
  impact?: string
  recommended_action?: string
  benchmark?: string
  business_impact?: string
  action?: string
  element_type?: string
  order_index: number
  background_data?: string
  image_url?: string
  sources?: Source[]
}

interface ReportElementProps {
  element: Element
  badge: { label: string; variant: "default" | "secondary" | "destructive" | "outline" }
  index: number
  reportId?: string  // Added reportId for chat functionality
}

export function ReportElement({ element, badge, index, reportId }: ReportElementProps) {
  const [isExpanded, setIsExpanded] = useState(false)
  const [showComments, setShowComments] = useState(false)
  const [showChat, setShowChat] = useState(false)
  const [showSources, setShowSources] = useState(false)

  const renderContent = (text: string) => {
    const parts = text.split(/(\*\*.*?\*\*)/)
    return parts.map((part, idx) => {
      if (part.startsWith("**") && part.endsWith("**")) {
        return (
          <strong key={idx} className="font-semibold text-foreground">
            {part.slice(2, -2)}
          </strong>
        )
      }
      return part
    })
  }

  return (
    <Card className={`transition-all ${isExpanded ? "ring-2 ring-primary shadow-lg" : "hover:shadow-md"}`}>
      <CardHeader>
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <Badge variant={badge.variant}>{badge.label}</Badge>
            </div>
            <CardTitle
              className="text-xl cursor-pointer hover:text-primary transition-colors text-balance"
              onClick={() => setIsExpanded(!isExpanded)}
            >
              {element.title}
            </CardTitle>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {element.image_url && (
          <div className="relative w-full h-64 rounded-lg overflow-hidden">
            <Image src={element.image_url || "/placeholder.svg"} alt={element.title} fill className="object-cover" />
          </div>
        )}

        {element.summary && (
          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-primary">Summary</h4>
            <p className="text-sm text-foreground leading-relaxed">{renderContent(element.summary)}</p>
          </div>
        )}

        {element.impact && (
          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-primary">Impact</h4>
            <p className="text-sm text-foreground leading-relaxed">{renderContent(element.impact)}</p>
          </div>
        )}

        {element.business_impact && (
          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-primary">Business Impact</h4>
            <p className="text-sm text-foreground leading-relaxed">{renderContent(element.business_impact)}</p>
          </div>
        )}

        {element.recommended_action && (
          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-primary">Recommended Action</h4>
            <p className="text-sm text-foreground leading-relaxed">{renderContent(element.recommended_action)}</p>
          </div>
        )}

        {element.action && (
          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-primary">Action</h4>
            <p className="text-sm text-foreground leading-relaxed">{renderContent(element.action)}</p>
          </div>
        )}

        {element.benchmark && (
          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-primary">Benchmark</h4>
            <p className="text-sm text-foreground leading-relaxed">{renderContent(element.benchmark)}</p>
          </div>
        )}

        {element.content && (
          <div className="space-y-4 pt-4 border-t">
            <h4 className="text-sm font-semibold text-muted-foreground">Detailed Analysis</h4>
            {element.content.split("\n").map((paragraph, idx) => (
              <p key={idx} className="text-sm text-foreground leading-relaxed text-pretty">
                {renderContent(paragraph)}
              </p>
            ))}
          </div>
        )}

        {element.sources && element.sources.length > 0 && (
          <div className="pt-4 border-t">
            <Button variant="ghost" size="sm" onClick={() => setShowSources(!showSources)} className="gap-2 -ml-2 mb-2">
              {showSources ? <ChevronUpIcon className="h-4 w-4" /> : <ChevronDownIcon className="h-4 w-4" />}
              {showSources ? "Hide" : "Show"} Sources & References ({element.sources.length})
            </Button>
            {showSources && (
              <ul className="space-y-2">
                {element.sources.map((source, idx) => (
                  <li key={idx}>
                    <a
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-primary hover:underline flex items-center gap-1 group"
                    >
                      <ExternalLinkIcon className="h-3 w-3 group-hover:translate-x-0.5 transition-transform" />
                      {source.title}
                    </a>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}

        <div className="flex items-center gap-2 pt-2 border-t">
          <VotingSection elementId={element.id} />

          <Button
            variant="ghost"
            size="sm"
            onClick={() => {
              setShowComments(!showComments)
              setShowChat(false)
            }}
            className="gap-2"
          >
            <MessageSquareIcon className="h-4 w-4" />
            Comments
          </Button>

          <Button
            variant="ghost"
            size="sm"
            onClick={() => {
              setShowChat(!showChat)
              setShowComments(false)
            }}
            className="gap-2"
          >
            <MessageCircleIcon className="h-4 w-4" />
            Ask follow-up 🪄
          </Button>

          <Button
            variant="default"
            size="sm"
            className="gap-2 bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-semibold shadow-md"
          >
            <div className="relative h-4 w-4">
              <TruckIcon className="h-4 w-4 absolute" />
              <TrendingDownIcon className="h-3 w-3 absolute -bottom-0.5 -right-0.5 text-red-300" />
            </div>
            Check the impact
          </Button>
        </div>

        {showComments && (
          <div className="pt-4 border-t">
            <CommentsSection elementId={element.id} />
          </div>
        )}

        {showChat && reportId && (
          <div className="pt-4 border-t">
            <ChatSection
              elementId={element.id}
              elementTitle={element.title}
              elementContent={element.content}
              backgroundData={element.background_data}
              reportId={reportId}
            />
          </div>
        )}

        {showChat && !reportId && (
          <div className="pt-4 border-t">
            <p className="text-sm text-muted-foreground">Chat is not available for this element.</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
