"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { PlusCircle, Loader2, CheckCircle, AlertCircle } from "lucide-react"
import { useGenerateReport } from "@/lib/hooks/use-api"

export function GenerateReportButton({ onSuccess }: { onSuccess?: (reportId: string) => void }) {
  const { generate, loading, error, reportId } = useGenerateReport()
  const [showSuccess, setShowSuccess] = useState(false)

  const handleGenerate = async () => {
    try {
      setShowSuccess(false)
      console.log("🚀 Starting report generation...")

      const result = await generate()

      console.log("✅ Report generated successfully:", result.report_id)

      setShowSuccess(true)

      // Call success callback to refresh list
      if (onSuccess) {
        onSuccess(result.report_id)
      }

      // Show success state for 3 seconds
      setTimeout(() => setShowSuccess(false), 3000)
    } catch (err) {
      console.error("❌ Report generation failed:", err)
      alert(`Report generation failed: ${error || "Unknown error"}`)
    }
  }

  return (
    <div className="flex flex-col gap-2">
      <Button
        onClick={handleGenerate}
        disabled={loading}
        size="lg"
        className="gap-2 bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-semibold shadow-lg hover:shadow-xl transition-all"
      >
        {loading ? (
          <>
            <Loader2 className="h-5 w-5 animate-spin" />
            Generating Report... (2-4 min)
          </>
        ) : showSuccess ? (
          <>
            <CheckCircle className="h-5 w-5" />
            Report Generated!
          </>
        ) : (
          <>
            <PlusCircle className="h-5 w-5" />
            Generate New Report
          </>
        )}
      </Button>

      {loading && (
        <p className="text-xs text-muted-foreground text-center">
          AI is analyzing compliance data... Please wait
        </p>
      )}

      {error && (
        <div className="flex items-center gap-2 text-xs text-red-500">
          <AlertCircle className="h-4 w-4" />
          <span>{error}</span>
        </div>
      )}
    </div>
  )
}
