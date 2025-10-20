"use client"

import { useEffect } from "react"
import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { TruckIcon, TrendingDownIcon, ArrowUpIcon, ArrowDownIcon, Loader2, FileText, Download } from "lucide-react"
import { useReports, useDownloadPDF } from "@/lib/hooks/use-api"
import { GenerateReportButton } from "@/components/generate-report-button"
import type { Report } from "@/lib/types"

export function ReportsList() {
  const { reports, total, loading, error, refetch } = useReports({ limit: 50, offset: 0 })
  const { download, loading: downloadLoading } = useDownloadPDF()

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

  const getRiskBadgeClass = (risk: string) => {
    const classes: Record<string, string> = {
      critical: "bg-red-500/10 text-red-400 border-red-500/20",
      high: "bg-orange-500/10 text-orange-400 border-orange-500/20",
      medium: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
      low: "bg-green-500/10 text-green-400 border-green-500/20",
    }
    return classes[risk] || "bg-muted text-muted-foreground"
  }

  const getStatusBadgeClass = (status: string) => {
    const classes: Record<string, string> = {
      approved: "bg-green-500/10 text-green-400 border-green-500/20",
      pending: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
      failed: "bg-red-500/10 text-red-400 border-red-500/20",
    }
    return classes[status] || "bg-muted text-muted-foreground"
  }

  const handleSuccess = (reportId: string) => {
    console.log("✅ New report generated:", reportId)
    // Refresh the reports list
    setTimeout(() => {
      refetch()
    }, 1000)
  }

  const handleDownloadPDF = async (reportId: string, companyName: string) => {
    try {
      await download(reportId, `${companyName}-compliance-report-${reportId.slice(0, 8)}.pdf`)
      console.log("✅ PDF downloaded successfully")
    } catch (err) {
      console.error("❌ PDF download failed:", err)
      alert("Failed to download PDF")
    }
  }

  if (loading && reports.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <Loader2 className="h-12 w-12 animate-spin text-primary mb-4" />
        <p className="text-muted-foreground">Loading reports...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <div className="text-red-500 mb-4">
          <svg
            className="h-12 w-12 mx-auto mb-2"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <p className="font-semibold">Failed to load reports</p>
          <p className="text-sm mt-2">{error}</p>
        </div>
        <Button onClick={() => refetch()} variant="outline">
          Try Again
        </Button>
      </div>
    )
  }

  return (
    <div>
      {/* Header with Generate Button */}
      <div className="mb-8 flex items-start justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-foreground mb-2">Intelligence Reports</h2>
          <p className="text-muted-foreground">
            AI-powered compliance insights • {total} report{total !== 1 ? "s" : ""} total
          </p>
        </div>
        <GenerateReportButton onSuccess={handleSuccess} />
      </div>

      {/* Reports Grid */}
      {reports.length === 0 ? (
        <Card className="border-dashed">
          <CardContent className="flex flex-col items-center justify-center py-20">
            <FileText className="h-16 w-16 text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">No reports yet</h3>
            <p className="text-muted-foreground text-center mb-6">
              Generate your first compliance report to get started
            </p>
            <GenerateReportButton onSuccess={handleSuccess} />
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-6">
          {reports.map((report: Report) => {
            const summary = report.content?.summary || {}
            const totalChanges = summary.total_changes || 0
            const overallRisk = summary.overall_risk || "medium"
            const keyTakeaways = summary.key_takeaways || []
            const legalChanges = report.content?.legal_changes || []
            const routeImpacts = report.content?.route_impacts || []

            return (
              <Card
                key={report.id}
                className="hover:shadow-lg hover:shadow-primary/10 transition-all border-border"
              >
                <CardHeader>
                  {/* Status and Risk Badges */}
                  <div className="flex items-start justify-between gap-4 mb-3">
                    <div className="flex gap-2">
                      <Badge className={getStatusBadgeClass(report.status)}>
                        {report.status.toUpperCase()}
                      </Badge>
                      <Badge className={getRiskBadgeClass(overallRisk)}>
                        {overallRisk.toUpperCase()} RISK
                      </Badge>
                    </div>
                    {new Date(report.generated_at) > new Date(Date.now() - 24 * 60 * 60 * 1000) && (
                      <Badge variant="secondary" className="shrink-0 gradient-primary text-white border-0">
                        New
                      </Badge>
                    )}
                  </div>

                  {/* Strategic Insights */}
                  {totalChanges > 0 && (
                    <div className="mb-4 pb-4 border-b border-border">
                      <p className="text-xs font-semibold text-muted-foreground mb-2">Strategic Insight:</p>
                      <div className="flex flex-wrap gap-3">
                        <div className="flex items-center gap-1.5 text-xs">
                          <span className="text-muted-foreground">Changes Identified:</span>
                          <span className="font-semibold text-foreground">{totalChanges}</span>
                        </div>
                        <div className="flex items-center gap-1.5 text-xs">
                          <span className="text-muted-foreground">Legal Updates:</span>
                          <span className="font-semibold text-foreground">{legalChanges.length}</span>
                        </div>
                        <div className="flex items-center gap-1.5 text-xs">
                          <span className="text-muted-foreground">Routes Affected:</span>
                          <span className="font-semibold text-foreground">{routeImpacts.length}</span>
                        </div>
                        <div className="flex items-center gap-1.5 text-xs">
                          <span className="text-muted-foreground">Sources:</span>
                          <span className="font-semibold text-foreground">
                            {report.search_metadata?.total_sources || 0}
                          </span>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Title */}
                  <Link href={`/report/${report.id}`} className="cursor-pointer">
                    <CardTitle className="text-xl font-bold mb-2 text-balance hover:text-primary transition-colors">
                      {report.company_name} - Compliance Report
                    </CardTitle>
                  </Link>

                  <CardDescription className="text-sm text-muted-foreground">
                    {formatDate(report.generated_at)} • Report ID: {report.id.slice(0, 8)}
                  </CardDescription>
                </CardHeader>

                <CardContent className="space-y-4">
                  {/* Key Takeaways */}
                  {keyTakeaways.length > 0 && (
                    <div>
                      <p className="text-sm font-semibold mb-2">Key Takeaways:</p>
                      <ul className="space-y-1">
                        {keyTakeaways.slice(0, 3).map((takeaway, idx) => (
                          <li key={idx} className="text-sm text-muted-foreground leading-relaxed text-pretty flex gap-2">
                            <span className="text-primary mt-1">•</span>
                            <span className="line-clamp-2">{takeaway}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Actions */}
                  <div className="flex items-center gap-2 pt-2">
                    <Link href={`/report/${report.id}`} className="cursor-pointer">
                      <Button
                        variant="default"
                        size="sm"
                        className="gap-2 bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-semibold shadow-md"
                      >
                        <div className="relative h-4 w-4">
                          <TruckIcon className="h-4 w-4 absolute" />
                          <TrendingDownIcon className="h-3 w-3 absolute -bottom-0.5 -right-0.5 text-red-300" />
                        </div>
                        View Full Report
                      </Button>
                    </Link>

                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDownloadPDF(report.id, report.company_name)}
                      disabled={downloadLoading}
                      className="gap-2"
                    >
                      {downloadLoading ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <Download className="h-4 w-4" />
                      )}
                      Download PDF
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>
      )}
    </div>
  )
}
