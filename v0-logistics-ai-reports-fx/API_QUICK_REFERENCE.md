# 🚀 API Quick Reference Card

## Backend: http://localhost:8000
## Frontend: http://localhost:3000

---

## 📋 Company Profile

```typescript
// Get profile
const profile = await api.getCompanyProfile()

// Update profile
const updated = await api.updateCompanyProfile(profile)

// Hook
const { profile, updateProfile, loading } = useCompanyProfile()
```

**Endpoints:**
- `GET /api/profile` - Get company profile
- `PUT /api/profile` - Update profile

---

## 📊 Reports

```typescript
// List all reports
const { reports, total } = await api.listReports({ limit: 50, offset: 0 })

// Get single report
const report = await api.getReport("report-id")

// Generate new report (takes 2-4 minutes)
const result = await api.generateReport({})
// Returns: { report_id, status, message }

// Search reports
const results = await api.searchReports("emissions standards")

// Delete report
await api.deleteReport("report-id")

// Hooks
const { reports, loading, error, refetch } = useReports()
const { report } = useReport(reportId)
const { generate, loading, reportId } = useGenerateReport()
const { deleteReport } = useDeleteReport()
const { results, search } = useSearchReports()
```

**Endpoints:**
- `POST /api/reports/generate` - Generate report
- `GET /api/reports?limit=50&offset=0` - List reports
- `GET /api/reports/{report_id}` - Get report
- `GET /api/reports/search?q=query` - Search reports
- `DELETE /api/reports/{report_id}` - Delete report

---

## 📄 PDF Operations

```typescript
// Download PDF
await api.downloadPDFToFile("report-id", "custom-name.pdf")

// Get PDF info
const info = await api.getPDFInfo("report-id")
// Returns: { report_id, metadata, available }

// Search PDFs
const results = await api.searchPDFs("border control")

// Hook
const { download, loading } = useDownloadPDF()
await download(reportId)
```

**Endpoints:**
- `GET /api/reports/{report_id}/pdf` - Download PDF
- `GET /api/reports/{report_id}/pdf/info` - Get PDF metadata
- `GET /api/reports/pdfs/search?q=query` - Search PDFs

---

## 💬 Chat

```typescript
// Get chat history
const history = await api.getChatHistory("report-id")

// Send message
const response = await api.sendChatMessage("report-id", "What are the main risks?")
// Returns: { message_id, content, sources, created_at }

// Get suggested questions
const suggestions = await api.getSuggestedQuestions("report-id")

// Clear history
await api.clearChatHistory("report-id")

// WebSocket (real-time)
const ws = api.connectChatWebSocket("report-id")
ws.onmessage = (event) => { /* handle message */ }

// Hook
const { messages, sendMessage, clearHistory, loading } = useChat(reportId)
```

**Endpoints:**
- `GET /api/chat/{report_id}/history` - Get history
- `POST /api/chat/{report_id}/message` - Send message
- `GET /api/chat/{report_id}/suggestions` - Get suggestions
- `DELETE /api/chat/{report_id}/history` - Clear history
- `WS /api/chat/{report_id}/ws` - WebSocket connection

---

## 🔧 Utilities

```typescript
// Health check
const health = await api.healthCheck()
// Returns: { status: "ok", timestamp: "..." }

// Get stats
const stats = await api.getStats()
// Returns: { total_reports, approved_reports, ... }

// Hook
const { stats, loading } = useAppStats()
```

**Endpoints:**
- `GET /api/health` - Health check
- `GET /api/stats` - App statistics

---

## 🎯 Common Workflows

### 1. Generate and View Report

```typescript
// Generate
const { generate } = useGenerateReport()
const result = await generate()

// Wait for completion (2-4 minutes)
// Then fetch report
const { report } = useReport(result.report_id)

// Download PDF
const { download } = useDownloadPDF()
await download(result.report_id)
```

### 2. List and Search Reports

```typescript
// List all
const { reports } = useReports({ limit: 20 })

// Search specific
const { search, results } = useSearchReports()
await search("Germany regulations")
```

### 3. Chat with Report

```typescript
const { messages, sendMessage } = useChat(reportId)

await sendMessage("What are the compliance deadlines?")
// Messages updated automatically
```

---

## 🔒 Types

All types are in `lib/types.ts`:

```typescript
import type {
  Report,
  ReportContent,
  LegalChange,
  RouteImpact,
  RecommendedAction,
  CompanyProfile,
  ChatMessage,
  // ... etc
} from "@/lib/types"
```

---

## 🛠️ Setup

### 1. Environment

Create `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2. Import API Client

```typescript
import { api } from "@/lib/api"
// or
import { useReports, useReport } from "@/lib/hooks/use-api"
```

### 3. Use in Components

```tsx
function MyComponent() {
  const { reports, loading, error } = useReports()

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return <div>{reports.map(report => ...)}</div>
}
```

---

## 📡 Response Formats

### Report Object
```json
{
  "id": "abc-123",
  "company_name": "EuroTrans Logistics",
  "status": "approved",
  "content": {
    "summary": { "total_changes": 5, "overall_risk": "medium", ... },
    "legal_changes": [...],
    "route_impacts": [...],
    "recommended_actions": [...]
  },
  "generated_at": "2025-01-18T10:30:00Z",
  "iteration_count": 2,
  "search_metadata": { "total_sources": 12, ... }
}
```

### Generate Response
```json
{
  "report_id": "abc-123",
  "status": "approved",
  "message": "Report generated successfully after 2 iteration(s)"
}
```

### Chat Response
```json
{
  "message_id": "msg-123",
  "content": "Based on the report...",
  "sources": ["Section 2.1", "Route Impact Analysis"],
  "created_at": "2025-01-18T10:35:00Z"
}
```

---

## 🐛 Error Handling

All API calls throw errors that can be caught:

```typescript
try {
  const result = await api.generateReport({})
} catch (error) {
  console.error("Failed:", error.message)
  // Show user-friendly message
}
```

With hooks, errors are returned:

```typescript
const { reports, error } = useReports()

if (error) {
  // Display error to user
  return <ErrorMessage message={error} />
}
```

---

## ⚡ Performance Notes

- **Report Generation**: 2-4 minutes (AI processing)
- **List Reports**: < 1 second
- **Get Single Report**: < 100ms
- **Chat Message**: 2-5 seconds (AI response)
- **PDF Download**: < 1 second (500KB file)

---

## 🎉 Quick Start

```bash
# Terminal 1: Start Backend
cd backend && python main.py

# Terminal 2: Start Frontend
cd v0-logistics-ai-reports-fx && npm run dev

# Open browser
# http://localhost:3000
```

That's it! Your frontend is connected to the backend! 🚀
