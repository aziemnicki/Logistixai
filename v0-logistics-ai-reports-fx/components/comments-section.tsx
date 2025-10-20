"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { SendIcon } from "lucide-react"
import { mockComments } from "@/lib/mock-data"

interface Comment {
  id: string
  user_name: string
  content: string
  created_at: string
}

interface CommentsSectionProps {
  elementId: string
}

export function CommentsSection({ elementId }: CommentsSectionProps) {
  const [comments, setComments] = useState<Comment[]>([])
  const [newComment, setNewComment] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const userName = "Janusz Trucker"

  useEffect(() => {
    const elementComments = mockComments[elementId] || []
    setComments(elementComments)
  }, [elementId])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newComment.trim()) return

    setIsLoading(true)

    setTimeout(() => {
      const newCommentObj: Comment = {
        id: `c${Date.now()}`,
        user_name: userName,
        content: newComment.trim(),
        created_at: new Date().toISOString(),
      }

      setComments([...comments, newCommentObj])
      setNewComment("")
      setIsLoading(false)
    }, 500)
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)
    const diffDays = Math.floor(diffMs / 86400000)

    if (diffMins < 1) return "just now"
    if (diffMins < 60) return `${diffMins}m ago`
    if (diffHours < 24) return `${diffHours}h ago`
    if (diffDays < 7) return `${diffDays}d ago`
    return new Intl.DateTimeFormat("en-US", {
      month: "short",
      day: "numeric",
    }).format(date)
  }

  return (
    <div className="space-y-4">
      <h3 className="font-semibold text-sm">Comments</h3>

      {/* Comments List */}
      <div className="space-y-3 max-h-96 overflow-y-auto">
        {comments.map((comment) => (
          <div key={comment.id} className="bg-muted/50 rounded-lg p-3">
            <div className="flex items-start gap-3">
              <Avatar className="h-8 w-8">
                <AvatarImage src="/professional-employee-portrait.jpg" alt={comment.user_name} />
                <AvatarFallback>
                  {comment.user_name
                    .split(" ")
                    .map((n) => n[0])
                    .join("")}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium">{comment.user_name}</span>
                  <span className="text-xs text-muted-foreground">{formatDate(comment.created_at)}</span>
                </div>
                <p className="text-sm text-foreground">{comment.content}</p>
              </div>
            </div>
          </div>
        ))}

        {comments.length === 0 && (
          <p className="text-sm text-muted-foreground text-center py-4">No comments yet. Be the first to comment!</p>
        )}
      </div>

      {/* Comment Form */}
      <form onSubmit={handleSubmit} className="space-y-2">
        <Textarea
          placeholder="Add a comment..."
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          className="min-h-20 resize-none"
          disabled={isLoading}
        />
        <div className="flex justify-end">
          <Button type="submit" size="sm" disabled={isLoading || !newComment.trim()}>
            <SendIcon className="h-4 w-4 mr-2" />
            Post Comment
          </Button>
        </div>
      </form>
    </div>
  )
}
