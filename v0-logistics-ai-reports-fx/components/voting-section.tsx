"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { ThumbsUpIcon, ThumbsDownIcon } from "lucide-react"
import { mockVotes } from "@/lib/mock-data"

interface VotingSectionProps {
  elementId: string
}

export function VotingSection({ elementId }: VotingSectionProps) {
  const [votes, setVotes] = useState<{ upvotes: number; downvotes: number }>({
    upvotes: 0,
    downvotes: 0,
  })
  const [userVote, setUserVote] = useState<"upvote" | "downvote" | null>(null)

  useEffect(() => {
    const voteData = mockVotes[elementId] || { upvotes: 0, downvotes: 0, userVote: null }
    setVotes({ upvotes: voteData.upvotes, downvotes: voteData.downvotes })
    setUserVote(voteData.userVote as "upvote" | "downvote" | null)
  }, [elementId])

  const handleVote = (voteType: "upvote" | "downvote") => {
    // Toggle vote
    if (userVote === voteType) {
      setUserVote(null)
      setVotes((prev) => ({
        ...prev,
        [voteType === "upvote" ? "upvotes" : "downvotes"]: Math.max(
          0,
          prev[voteType === "upvote" ? "upvotes" : "downvotes"] - 1,
        ),
      }))
    } else {
      // Remove old vote if exists
      if (userVote) {
        setVotes((prev) => ({
          ...prev,
          [userVote === "upvote" ? "upvotes" : "downvotes"]: Math.max(
            0,
            prev[userVote === "upvote" ? "upvotes" : "downvotes"] - 1,
          ),
        }))
      }
      // Add new vote
      setUserVote(voteType)
      setVotes((prev) => ({
        ...prev,
        [voteType === "upvote" ? "upvotes" : "downvotes"]: prev[voteType === "upvote" ? "upvotes" : "downvotes"] + 1,
      }))
    }
  }

  return (
    <div className="flex items-center gap-2">
      <Button
        variant={userVote === "upvote" ? "default" : "ghost"}
        size="sm"
        onClick={() => handleVote("upvote")}
        className="gap-1"
      >
        <ThumbsUpIcon className="h-4 w-4" />
        <span className="text-xs">{votes.upvotes}</span>
      </Button>

      <Button
        variant={userVote === "downvote" ? "destructive" : "ghost"}
        size="sm"
        onClick={() => handleVote("downvote")}
        className="gap-1"
      >
        <ThumbsDownIcon className="h-4 w-4" />
        <span className="text-xs">{votes.downvotes}</span>
      </Button>
    </div>
  )
}
