/**
 * TypeScript types matching the backend API models
 * These correspond to the Pydantic models in simplified_models.py
 */

// Company Profile Types
export interface Location {
  city: string
  country: string
  country_code: string
}

export interface Route {
  origin: Location
  destination: Location
  transit_countries: string[]
  frequency: string
}

export interface Vehicle {
  vehicle_type: string
  count: number
  specifications: string[]
}

export interface CompanyProfile {
  company_name: string
  headquarters: Location
  routes: Route[]
  fleet: Vehicle[]
  cargo_categories: string[]
}

// Report Types
export interface ReportSummary {
  total_changes: number
  overall_risk: "critical" | "high" | "medium" | "low"
  key_takeaways: string[]
}

export interface LegalChange {
  title: string
  description: string
  effective_date: string | null
  affected_countries: string[]
  risk_level: "critical" | "high" | "medium" | "low"
  source_url: string
}

export interface RouteImpact {
  route_name: string
  impact_description: string
  risk_level: "critical" | "high" | "medium" | "low"
  recommended_actions: string[]
}

export interface RecommendedAction {
  priority: "critical" | "high" | "medium" | "low"
  action: string
  deadline: string | null
}

export interface ReportContent {
  summary: ReportSummary
  legal_changes: LegalChange[]
  route_impacts: RouteImpact[]
  recommended_actions: RecommendedAction[]
}

export interface ValidationHistory {
  iteration: number
  is_approved: boolean
  quality_score: number
  feedback: string
  issues: string[]
  validated_at: string
}

export interface SearchMetadata {
  total_sources: number
  queries_used: string[]
}

export interface Report {
  id: string
  company_name: string
  status: "approved" | "pending" | "failed"
  content: ReportContent
  generated_at: string
  validation_history: ValidationHistory[]
  iteration_count: number
  search_metadata: SearchMetadata
  pdf_path?: string
}

// API Request/Response Types
export interface GenerateReportRequest {
  company_profile?: CompanyProfile
}

export interface GenerateReportResponse {
  report_id: string
  status: string
  message: string
}

export interface ReportListResponse {
  reports: Report[]
  total: number
}

export interface SearchReportsResponse {
  query: string
  results: Report[]
  total: number
}

// PDF Types
export interface PDFMetadata {
  company_name: string
  generated_at: string
  status: string
  file_size_kb?: number
  format: string
  pdf_path: string
}

export interface PDFInfo {
  report_id: string
  metadata: PDFMetadata
  available: boolean
}

// Chat Types
export interface ChatMessage {
  id: string
  role: "user" | "assistant"
  content: string
  sources?: string[]
  created_at: string
}

export interface ChatHistory {
  report_id: string
  messages: ChatMessage[]
}

export interface ChatMessageRequest {
  message: string
}

export interface ChatMessageResponse {
  message_id: string
  content: string
  sources: string[]
  created_at: string
}

export interface SuggestedQuestions {
  report_id: string
  suggestions: string[]
}

// Stats Types
export interface AppStats {
  total_reports: number
  reports_in_chromadb: number
  approved_reports: number
  failed_reports: number
  data_directory: string
  chromadb_path: string
}

// Health Check
export interface HealthCheckResponse {
  status: string
  timestamp: string
}

// Error Response
export interface ErrorResponse {
  detail: string
}

// WebSocket Message Types
export interface WSMessage {
  type: "message" | "error" | "info"
  message_id?: string
  content?: string
  sources?: string[]
  created_at?: string
  error?: string
  message?: string
}
