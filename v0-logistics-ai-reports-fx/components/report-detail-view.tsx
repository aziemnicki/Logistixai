"use client"

import { useReport, useDownloadPDF } from "@/lib/hooks/use-api"
import { ReportElement } from "@/components/report-element"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Loader2, Download, FileText, AlertCircle, CheckCircle, Clock } from "lucide-react"
import type { Report, LegalChange, RouteImpact, RecommendedAction } from "@/lib/types"

interface ReportDetailViewProps {
  reportId: string
}

export function ReportDetailView({ reportId }: ReportDetailViewProps) {
  const { report, loading, error, refetch } = useReport(reportId)
  const { download, loading: downloadLoading } = useDownloadPDF()

  // Loading state
  if (loading && !report) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <Loader2 className="h-12 w-12 animate-spin text-primary mb-4" />
        <p className="text-muted-foreground">Loading report...</p>
      </div>
    )
  }

  // Error state
  if (error) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <div className="text-red-500 mb-4 text-center">
          <AlertCircle className="h-12 w-12 mx-auto mb-2" />
          <p className="font-semibold">Failed to load report</p>
          <p className="text-sm mt-2">{error}</p>
        </div>
        <Button onClick={() => refetch()} variant="outline">
          Try Again
        </Button>
      </div>
    )
  }

  // Report not found
  if (!report) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <FileText className="h-12 w-12 text-muted-foreground mb-4" />
        <p className="text-muted-foreground">Report not found</p>
      </div>
    )
  }

  // Format date
  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(date)
  }

  // Get status badge styling
  const getStatusBadgeClass = (status: string) => {
    const classes: Record<string, string> = {
      approved: "bg-green-500/10 text-green-400 border-green-500/20",
      pending: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
      failed: "bg-red-500/10 text-red-400 border-red-500/20",
    }
    return classes[status] || "bg-muted text-muted-foreground"
  }

  // Get risk badge styling
  const getRiskBadgeClass = (risk: string) => {
    const classes: Record<string, string> = {
      critical: "bg-red-500/10 text-red-400 border-red-500/20",
      high: "bg-orange-500/10 text-orange-400 border-orange-500/20",
      medium: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
      low: "bg-green-500/10 text-green-400 border-green-500/20",
    }
    return classes[risk] || "bg-muted text-muted-foreground"
  }

  // Download PDF handler
  const handleDownloadPDF = async () => {
    try {
      await download(reportId, `${report.company_name}-compliance-report-${reportId.slice(0, 8)}.pdf`)
    } catch (err) {
      console.error("❌ PDF download failed:", err)
      alert("Failed to download PDF")
    }
  }

  // Convert backend data to ReportElement format
  const convertToElements = () => {
    const elements: any[] = []

    // Add summary as first element
    if (report.content?.summary) {
      const summaryContent = report.content.summary.key_takeaways?.join("\n\n") || "No detailed summary available."
      elements.push({
        id: `summary-${reportId}`,
        title: "Executive Summary",
        category: "summary",
        summary: `${report.content.summary.total_changes} regulatory and operational changes identified with ${report.content.summary.overall_risk} overall risk level`,
        content: summaryContent,
        order_index: 0,
        sources: [],
      })
    }

    // Add legal changes as elements
    report.content?.legal_changes?.forEach((change: LegalChange, idx: number) => {
      const content = change.description || "No detailed description available."
      elements.push({
        id: `legal-${idx}`,
        title: change.title || "Legal Change",
        category: "regulatory",
        summary: change.description || "",
        impact: `Effective Date: ${change.effective_date || "TBD"} | Affected Countries: ${change.affected_countries?.join(", ") || "N/A"}`,
        content: content,
        recommended_action: `Risk Level: ${change.risk_level?.toUpperCase() || "MEDIUM"}`,
        order_index: idx + 1,
        sources: change.source_url ? [{ title: "Source", url: change.source_url }] : [],
      })
    })

    // Add route impacts as elements
    report.content?.route_impacts?.forEach((impact: RouteImpact, idx: number) => {
      const content = impact.impact_description || "No detailed impact description available."
      elements.push({
        id: `route-${idx}`,
        title: impact.route_name || "Route Impact",
        category: "operations",
        summary: impact.impact_description || "",
        impact: `Affected Segments: ${impact.affected_segments?.join(", ") || "N/A"}`,
        business_impact: impact.estimated_cost_impact || "Cost impact under assessment",
        recommended_action: impact.alternative_routes?.join("; ") || "Review alternative routing options",
        content: content,
        order_index: (report.content?.legal_changes?.length || 0) + idx + 1,
        sources: [],
      })
    })

    // Recommended actions section removed per user request

    return elements
  }

  // Get badge for element type
  const getElementTypeBadge = (category: string) => {
    const badges: Record<string, { label: string; variant: "default" | "secondary" | "destructive" | "outline" }> = {
      summary: { label: "Summary", variant: "default" },
      business_forecast: { label: "Action Required", variant: "default" },
      operations: { label: "Route Impact", variant: "secondary" },
      regulatory: { label: "Legal Change", variant: "destructive" },
      technology: { label: "Technology", variant: "outline" },
    }
    return badges[category] || { label: category, variant: "outline" }
  }

  const elements = convertToElements()
  const summary = report.content?.summary || {}
  const overallRisk = summary.overall_risk || "medium"

  return (
    <div>
      {/* Report Header */}
      <div className="border-b bg-card">
        <div className="container mx-auto px-6 py-8">
          <div className="max-w-4xl">
            {/* Status and Metadata */}
            <div className="flex items-center gap-2 mb-4 flex-wrap">
              <Badge className={getStatusBadgeClass(report.status)}>
                {report.status === "approved" && <CheckCircle className="h-3 w-3 mr-1" />}
                {report.status === "pending" && <Clock className="h-3 w-3 mr-1" />}
                {report.status === "failed" && <AlertCircle className="h-3 w-3 mr-1" />}
                {report.status.toUpperCase()}
              </Badge>
              <Badge className={getRiskBadgeClass(overallRisk)}>
                {overallRisk.toUpperCase()} RISK
              </Badge>
              <span className="text-sm text-muted-foreground">•</span>
              <span className="text-sm text-muted-foreground">
                {summary.total_changes || 0} changes identified
              </span>
              <span className="text-sm text-muted-foreground">•</span>
              <span className="text-sm text-muted-foreground">
                {report.search_metadata?.total_sources || 0} sources analyzed
              </span>
            </div>

            {/* Title and Date */}
            <p className="text-sm text-muted-foreground mb-3">{formatDate(report.generated_at)}</p>
            <h1 className="text-3xl font-bold text-foreground mb-4 text-balance">
              {report.company_name} - Compliance Intelligence Report
            </h1>

            {/* Key Takeaways */}
            {summary.key_takeaways && summary.key_takeaways.length > 0 && (
              <div className="bg-muted/50 rounded-lg p-4 mb-4">
                <h3 className="text-sm font-semibold mb-2">Key Takeaways:</h3>
                <ul className="space-y-1">
                  {summary.key_takeaways.map((takeaway: string, idx: number) => (
                    <li key={idx} className="text-sm text-foreground leading-relaxed flex gap-2">
                      <span className="text-primary mt-0.5">•</span>
                      <span>{takeaway}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex gap-3 mt-6">
              <Button
                onClick={handleDownloadPDF}
                disabled={downloadLoading}
                size="lg"
                className="gap-2 bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-semibold shadow-lg hover:shadow-xl transition-all"
              >
                {downloadLoading ? (
                  <>
                    <Loader2 className="h-5 w-5 animate-spin" />
                    Downloading...
                  </>
                ) : (
                  <>
                    <Download className="h-5 w-5" />
                    Download PDF Report
                  </>
                )}
              </Button>

              <Button onClick={() => refetch()} variant="outline" size="lg">
                Refresh Data
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Report Content */}
      <main className="container mx-auto px-6 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Statistics Overview */}
          <Card className="mb-8">
            <CardContent className="pt-6">
              <h3 className="text-lg font-semibold mb-4">Report Statistics</h3>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <p className="text-sm text-muted-foreground">Total Changes</p>
                  <p className="text-2xl font-bold text-foreground">{summary.total_changes || 0}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Legal Updates</p>
                  <p className="text-2xl font-bold text-foreground">{report.content?.legal_changes?.length || 0}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Routes Affected</p>
                  <p className="text-2xl font-bold text-foreground">{report.content?.route_impacts?.length || 0}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Report Elements */}
          <div className="space-y-8">
            {elements.map((element: any, index: number) => {
              const badge = getElementTypeBadge(element.category)
              return <ReportElement key={element.id} element={element} badge={badge} index={index} reportId={reportId} />
            })}
          </div>

          {elements.length === 0 && (
            <Card className="border-dashed">
              <CardContent className="flex flex-col items-center justify-center py-20">
                <FileText className="h-16 w-16 text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold mb-2">No report content available</h3>
                <p className="text-muted-foreground text-center">
                  This report may still be processing or encountered an error during generation.
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </main>
    </div>
  )
}
