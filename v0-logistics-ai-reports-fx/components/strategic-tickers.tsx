"use client"

import { TrendingUpIcon, TrendingDownIcon } from "lucide-react"
import { useEffect, useState } from "react"

interface Ticker {
  label: string
  value: string
  trend: "up" | "down"
  change: string
}

export function StrategicTickers() {
  const [tickers, setTickers] = useState<Ticker[]>([
    { label: "EU Freight Rate Index", value: "€1.42/km", trend: "up", change: "+3.2%" },
    { label: "Diesel Price (EU avg)", value: "€1.68/L", trend: "down", change: "-1.8%" },
    { label: "Border Wait Time", value: "4.2h", trend: "up", change: "+12%" },
  ])

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setTickers((prev) =>
        prev.map((ticker) => ({
          ...ticker,
          // Randomly flip trend for demo purposes
          trend: Math.random() > 0.7 ? (ticker.trend === "up" ? "down" : "up") : ticker.trend,
        })),
      )
    }, 10000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="flex items-center gap-4 text-xs">
      <span className="text-muted-foreground font-medium">Strategic insights detected:</span>
      <div className="flex items-center gap-4">
        {tickers.map((ticker, index) => (
          <div key={index} className="flex items-center gap-1.5">
            <span className="text-muted-foreground text-xs">{ticker.label}</span>
            <span className="text-foreground font-medium text-xs">{ticker.value}</span>
            <div className={`flex items-center gap-0.5 ${ticker.trend === "up" ? "text-green-500" : "text-red-500"}`}>
              {ticker.trend === "up" ? (
                <TrendingUpIcon className="h-3 w-3" />
              ) : (
                <TrendingDownIcon className="h-3 w-3" />
              )}
              <span className="text-xs font-medium">{ticker.change}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
