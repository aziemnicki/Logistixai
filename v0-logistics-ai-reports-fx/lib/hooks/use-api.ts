/**
 * React Hooks for API Calls
 * Provides easy-to-use hooks for frontend components
 */

import { useState, useEffect, useCallback, useRef, useMemo } from "react"
import { LogisticsAPIClient } from "../api"
import type { Report, ReportListResponse, CompanyProfile, AppStats } from "../types"
import { useAPIKey } from "../api-key-context"

/**
 * Hook to get API client with current API key
 */
function useApiClient() {
  const { apiKey } = useAPIKey()
  return useMemo(() => new LogisticsAPIClient(undefined, apiKey), [apiKey])
}

/**
 * Hook to fetch all reports with loading and error states
 * Only fetches ONCE on mount, then only when refetch() is explicitly called
 */
export function useReports(options?: { limit?: number; offset?: number; autoFetch?: boolean }) {
  const api = useApiClient()
  const [reports, setReports] = useState<Report[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Track if we've already fetched to prevent continuous polling
  const hasFetchedRef = useRef(false)

  // Extract values to stable variables
  const limit = options?.limit
  const offset = options?.offset
  const autoFetch = options?.autoFetch !== false

  const fetchReports = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const result = await api.listReports({ limit, offset })
      setReports(result.reports)
      setTotal(result.total)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch reports")
    } finally {
      setLoading(false)
    }
  }, [api, limit, offset])

  // Only fetch ONCE on mount if autoFetch is true
  useEffect(() => {
    if (autoFetch && !hasFetchedRef.current) {
      hasFetchedRef.current = true
      fetchReports()
    }
  }, []) // Empty dependency array = only runs once on mount

  return { reports, total, loading, error, refetch: fetchReports }
}

/**
 * Hook to fetch a single report by ID
 * Only fetches ONCE when reportId changes, then only when refetch() is explicitly called
 */
export function useReport(reportId: string | null) {
  const api = useApiClient()
  const [report, setReport] = useState<Report | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Track the last fetched ID to prevent refetching the same report
  const lastFetchedIdRef = useRef<string | null>(null)

  const fetchReport = useCallback(async () => {
    if (!reportId) return

    setLoading(true)
    setError(null)

    try {
      const result = await api.getReport(reportId)
      setReport(result)
      lastFetchedIdRef.current = reportId
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch report")
    } finally {
      setLoading(false)
    }
  }, [api, reportId])

  // Only fetch when reportId changes (not on every render)
  useEffect(() => {
    if (reportId && reportId !== lastFetchedIdRef.current) {
      fetchReport()
    }
  }, [reportId]) // Only depend on reportId, not fetchReport

  return { report, loading, error, refetch: fetchReport }
}

/**
 * Hook to generate a new report
 */
export function useGenerateReport() {
  const api = useApiClient()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [reportId, setReportId] = useState<string | null>(null)

  const generate = useCallback(async () => {
    setLoading(true)
    setError(null)
    setReportId(null)

    try {
      const result = await api.generateReport({})
      setReportId(result.report_id)
      return result
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : "Failed to generate report"
      setError(errorMsg)
      throw err
    } finally {
      setLoading(false)
    }
  }, [api])

  return { generate, loading, error, reportId }
}

/**
 * Hook to delete a report
 */
export function useDeleteReport() {
  const api = useApiClient()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const deleteReport = useCallback(async (reportId: string) => {
    setLoading(true)
    setError(null)

    try {
      await api.deleteReport(reportId)
      return true
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : "Failed to delete report"
      setError(errorMsg)
      return false
    } finally {
      setLoading(false)
    }
  }, [api])

  return { deleteReport, loading, error }
}

/**
 * Hook to search reports
 */
export function useSearchReports() {
  const api = useApiClient()
  const [results, setResults] = useState<Report[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const search = useCallback(async (query: string, limit: number = 10) => {
    if (!query.trim()) {
      setResults([])
      return
    }

    setLoading(true)
    setError(null)

    try {
      const result = await api.searchReports(query, limit)
      setResults(result.results)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Search failed")
    } finally {
      setLoading(false)
    }
  }, [api])

  return { results, search, loading, error }
}

/**
 * Hook to fetch company profile
 * Only fetches ONCE on mount
 */
export function useCompanyProfile() {
  const api = useApiClient()
  const [profile, setProfile] = useState<CompanyProfile | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Track if we've already fetched
  const hasFetchedRef = useRef(false)

  const fetchProfile = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const result = await api.getCompanyProfile()
      setProfile(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch profile")
    } finally {
      setLoading(false)
    }
  }, [api])

  const updateProfile = useCallback(async (newProfile: CompanyProfile) => {
    setLoading(true)
    setError(null)

    try {
      const result = await api.updateCompanyProfile(newProfile)
      setProfile(result)
      return true
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update profile")
      return false
    } finally {
      setLoading(false)
    }
  }, [api])

  // Only fetch ONCE on mount
  useEffect(() => {
    if (!hasFetchedRef.current) {
      hasFetchedRef.current = true
      fetchProfile()
    }
  }, [])

  return { profile, updateProfile, loading, error, refetch: fetchProfile }
}

/**
 * Hook to fetch app statistics
 * Only fetches ONCE on mount
 */
export function useAppStats() {
  const api = useApiClient()
  const [stats, setStats] = useState<AppStats | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Track if we've already fetched
  const hasFetchedRef = useRef(false)

  const fetchStats = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const result = await api.getStats()
      setStats(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch stats")
    } finally {
      setLoading(false)
    }
  }, [api])

  // Only fetch ONCE on mount
  useEffect(() => {
    if (!hasFetchedRef.current) {
      hasFetchedRef.current = true
      fetchStats()
    }
  }, [])

  return { stats, loading, error, refetch: fetchStats }
}

/**
 * Hook for chat functionality
 * Only fetches history ONCE when reportId changes
 */
export function useChat(reportId: string | null) {
  const api = useApiClient()
  const [messages, setMessages] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Track the last fetched report ID
  const lastFetchedIdRef = useRef<string | null>(null)

  const fetchHistory = useCallback(async () => {
    if (!reportId) return

    setLoading(true)
    setError(null)

    try {
      const history = await api.getChatHistory(reportId)
      setMessages(history.messages || [])
      lastFetchedIdRef.current = reportId
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch chat history")
    } finally {
      setLoading(false)
    }
  }, [api, reportId])

  const sendMessage = useCallback(
    async (message: string) => {
      if (!reportId) return

      setLoading(true)
      setError(null)

      try {
        const response = await api.sendChatMessage(reportId, message)

        // Add user message
        setMessages((prev) => [
          ...prev,
          {
            id: `user_${Date.now()}`,
            role: "user",
            content: message,
            created_at: new Date().toISOString(),
          },
        ])

        // Add assistant message
        setMessages((prev) => [
          ...prev,
          {
            id: response.message_id,
            role: "assistant",
            content: response.content,
            sources: response.sources,
            created_at: response.created_at,
          },
        ])

        return response
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to send message")
        throw err
      } finally {
        setLoading(false)
      }
    },
    [api, reportId]
  )

  const clearHistory = useCallback(async () => {
    if (!reportId) return

    try {
      await api.clearChatHistory(reportId)
      setMessages([])
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to clear history")
    }
  }, [api, reportId])

  // Only fetch when reportId changes
  useEffect(() => {
    if (reportId && reportId !== lastFetchedIdRef.current) {
      fetchHistory()
    }
  }, [reportId])

  return { messages, sendMessage, clearHistory, loading, error, refetch: fetchHistory }
}

/**
 * Hook to download PDF
 */
export function useDownloadPDF() {
  const api = useApiClient()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const download = useCallback(async (reportId: string, filename?: string) => {
    setLoading(true)
    setError(null)

    try {
      await api.downloadPDFToFile(reportId, filename)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to download PDF")
    } finally {
      setLoading(false)
    }
  }, [api])

  return { download, loading, error }
}
