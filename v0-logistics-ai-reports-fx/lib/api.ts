/**
 * API Client for Backend Communication
 * Maps all backend endpoints (port 8000) to frontend calls
 */

import type {
  CompanyProfile,
  GenerateReportRequest,
  GenerateReportResponse,
  Report,
  ReportListResponse,
  SearchReportsResponse,
  PDFInfo,
  ChatHistory,
  ChatMessageRequest,
  ChatMessageResponse,
  SuggestedQuestions,
  AppStats,
  HealthCheckResponse,
  ErrorResponse,
} from "./types"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

/**
 * Helper function to handle API errors
 */
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error: ErrorResponse = await response.json().catch(() => ({
      detail: `HTTP ${response.status}: ${response.statusText}`,
    }))
    throw new Error(error.detail)
  }
  return response.json()
}

/**
 * API Client Class
 */
export class LogisticsAPIClient {
  private baseUrl: string
  private apiKey: string | null

  constructor(baseUrl: string = API_BASE_URL, apiKey: string | null = null) {
    this.baseUrl = baseUrl
    this.apiKey = apiKey
  }

  /**
   * Get headers for API requests
   */
  private getHeaders(additionalHeaders: Record<string, string> = {}): Record<string, string> {
    const headers: Record<string, string> = {
      ...additionalHeaders,
    }

    if (this.apiKey) {
      headers["X-API-Key"] = this.apiKey
    }

    return headers
  }

  // ============================================================================
  // COMPANY PROFILE ENDPOINTS
  // ============================================================================

  /**
   * GET /api/profile
   * Get company profile
   */
  async getCompanyProfile(): Promise<CompanyProfile> {
    const response = await fetch(`${this.baseUrl}/api/profile`)
    return handleResponse<CompanyProfile>(response)
  }

  /**
   * PUT /api/profile
   * Update company profile
   */
  async updateCompanyProfile(profile: CompanyProfile): Promise<CompanyProfile> {
    const response = await fetch(`${this.baseUrl}/api/profile`, {
      method: "PUT",
      headers: this.getHeaders({ "Content-Type": "application/json" }),
      body: JSON.stringify(profile),
    })
    return handleResponse<CompanyProfile>(response)
  }

  // ============================================================================
  // REPORT ENDPOINTS
  // ============================================================================

  /**
   * POST /api/reports/generate
   * Generate a new compliance report
   */
  async generateReport(request: GenerateReportRequest = {}): Promise<GenerateReportResponse> {
    const response = await fetch(`${this.baseUrl}/api/reports/generate`, {
      method: "POST",
      headers: this.getHeaders({ "Content-Type": "application/json" }),
      body: JSON.stringify(request),
    })
    return handleResponse<GenerateReportResponse>(response)
  }

  /**
   * GET /api/reports
   * Get list of all reports with pagination
   */
  async listReports(params?: { limit?: number; offset?: number }): Promise<ReportListResponse> {
    const queryParams = new URLSearchParams()
    if (params?.limit) queryParams.set("limit", params.limit.toString())
    if (params?.offset) queryParams.set("offset", params.offset.toString())

    const url = `${this.baseUrl}/api/reports${queryParams.toString() ? `?${queryParams}` : ""}`
    const response = await fetch(url)
    return handleResponse<ReportListResponse>(response)
  }

  /**
   * GET /api/reports/search
   * Search reports using semantic search
   */
  async searchReports(query: string, limit: number = 10): Promise<SearchReportsResponse> {
    const params = new URLSearchParams({ q: query, limit: limit.toString() })
    const response = await fetch(`${this.baseUrl}/api/reports/search?${params}`)
    return handleResponse<SearchReportsResponse>(response)
  }

  /**
   * GET /api/reports/{report_id}
   * Get a specific report by ID
   */
  async getReport(reportId: string): Promise<Report> {
    const response = await fetch(`${this.baseUrl}/api/reports/${reportId}`)
    return handleResponse<Report>(response)
  }

  /**
   * DELETE /api/reports/{report_id}
   * Delete a report
   */
  async deleteReport(reportId: string): Promise<{ message: string }> {
    const response = await fetch(`${this.baseUrl}/api/reports/${reportId}`, {
      method: "DELETE",
    })
    return handleResponse<{ message: string }>(response)
  }

  // ============================================================================
  // PDF ENDPOINTS
  // ============================================================================

  /**
   * GET /api/reports/{report_id}/pdf
   * Download PDF report (returns blob)
   */
  async downloadReportPDF(reportId: string): Promise<Blob> {
    const response = await fetch(`${this.baseUrl}/api/reports/${reportId}/pdf`)
    if (!response.ok) {
      throw new Error(`Failed to download PDF: ${response.statusText}`)
    }
    return response.blob()
  }

  /**
   * Helper to download PDF and trigger browser download
   */
  async downloadPDFToFile(reportId: string, filename?: string): Promise<void> {
    const blob = await this.downloadReportPDF(reportId)
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = filename || `compliance_report_${reportId}.pdf`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  }

  /**
   * GET /api/reports/{report_id}/pdf/info
   * Get PDF metadata
   */
  async getPDFInfo(reportId: string): Promise<PDFInfo> {
    const response = await fetch(`${this.baseUrl}/api/reports/${reportId}/pdf/info`)
    return handleResponse<PDFInfo>(response)
  }

  /**
   * GET /api/reports/pdfs/search
   * Search PDFs using semantic search
   */
  async searchPDFs(query: string, limit: number = 10): Promise<SearchReportsResponse> {
    const params = new URLSearchParams({ q: query, limit: limit.toString() })
    const response = await fetch(`${this.baseUrl}/api/reports/pdfs/search?${params}`)
    return handleResponse<SearchReportsResponse>(response)
  }

  // ============================================================================
  // CHAT ENDPOINTS
  // ============================================================================

  /**
   * GET /api/chat/{report_id}/history
   * Get chat history for a report
   */
  async getChatHistory(reportId: string): Promise<ChatHistory> {
    const response = await fetch(`${this.baseUrl}/api/chat/${reportId}/history`)
    return handleResponse<ChatHistory>(response)
  }

  /**
   * POST /api/chat/{report_id}/message
   * Send a chat message
   */
  async sendChatMessage(reportId: string, message: string): Promise<ChatMessageResponse> {
    const response = await fetch(`${this.baseUrl}/api/chat/${reportId}/message`, {
      method: "POST",
      headers: this.getHeaders({ "Content-Type": "application/json" }),
      body: JSON.stringify({ message } as ChatMessageRequest),
    })
    return handleResponse<ChatMessageResponse>(response)
  }

  /**
   * GET /api/chat/{report_id}/suggestions
   * Get suggested follow-up questions
   */
  async getSuggestedQuestions(reportId: string): Promise<SuggestedQuestions> {
    const response = await fetch(`${this.baseUrl}/api/chat/${reportId}/suggestions`, {
      headers: this.getHeaders(),
    })
    return handleResponse<SuggestedQuestions>(response)
  }

  /**
   * DELETE /api/chat/{report_id}/history
   * Clear chat history
   */
  async clearChatHistory(reportId: string): Promise<{ message: string }> {
    const response = await fetch(`${this.baseUrl}/api/chat/${reportId}/history`, {
      method: "DELETE",
    })
    return handleResponse<{ message: string }>(response)
  }

  /**
   * Connect to WebSocket for real-time chat
   * ws://localhost:8000/api/chat/{report_id}/ws
   */
  connectChatWebSocket(reportId: string): WebSocket {
    const wsUrl = this.baseUrl.replace("http://", "ws://").replace("https://", "wss://")
    return new WebSocket(`${wsUrl}/api/chat/${reportId}/ws`)
  }

  // ============================================================================
  // UTILITY ENDPOINTS
  // ============================================================================

  /**
   * GET /api/health
   * Health check
   */
  async healthCheck(): Promise<HealthCheckResponse> {
    const response = await fetch(`${this.baseUrl}/api/health`)
    return handleResponse<HealthCheckResponse>(response)
  }

  /**
   * GET /api/stats
   * Get application statistics
   */
  async getStats(): Promise<AppStats> {
    const response = await fetch(`${this.baseUrl}/api/stats`)
    return handleResponse<AppStats>(response)
  }
}

// Export singleton instance
export const api = new LogisticsAPIClient()

// Export default
export default api
