# 🔌 Backend Integration Guide

## Overview

This document explains how the **Frontend** (Next.js, port 3000) connects to the **Backend** (FastAPI, port 8000).

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND                          │
│          Next.js App (localhost:3000)               │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │          Components (React/TSX)              │  │
│  │   - page.tsx                                 │  │
│  │   - report/[id]/page.tsx                     │  │
│  │   - components/...                           │  │
│  └─────────────────┬────────────────────────────┘  │
│                    │                                 │
│  ┌─────────────────▼────────────────────────────┐  │
│  │       Hooks (lib/hooks/use-api.ts)          │  │
│  │   - useReports()                             │  │
│  │   - useReport(id)                            │  │
│  │   - useGenerateReport()                      │  │
│  │   - useChat(reportId)                        │  │
│  └─────────────────┬────────────────────────────┘  │
│                    │                                 │
│  ┌─────────────────▼────────────────────────────┐  │
│  │       API Client (lib/api.ts)               │  │
│  │   - LogisticsAPIClient                       │  │
│  │   - Handles all HTTP requests                │  │
│  └─────────────────┬────────────────────────────┘  │
│                    │                                 │
└────────────────────┼─────────────────────────────────┘
                     │
                     │ HTTP/WebSocket
                     │ (localhost:8000)
                     ▼
┌─────────────────────────────────────────────────────┐
│                    BACKEND                          │
│           FastAPI App (localhost:8000)              │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │           Routes (routes.py)                 │  │
│  │   - /api/profile                             │  │
│  │   - /api/reports                             │  │
│  │   - /api/chat                                │  │
│  │   - /api/health                              │  │
│  └─────────────────┬────────────────────────────┘  │
│                    │                                 │
│  ┌─────────────────▼────────────────────────────┐  │
│  │      Services (services/)                    │  │
│  │   - report_service.py                        │  │
│  │   - chat_service.py                          │  │
│  │   - pdf_service.py                           │  │
│  └─────────────────┬────────────────────────────┘  │
│                    │                                 │
│  ┌─────────────────▼────────────────────────────┐  │
│  │       AI Agents (agents/)                    │  │
│  │   - search_agent.py                          │  │
│  │   - report_agent.py                          │  │
│  │   - validator_agent.py                       │  │
│  │   - chat_agent.py                            │  │
│  └─────────────────┬────────────────────────────┘  │
│                    │                                 │
│  ┌─────────────────▼────────────────────────────┐  │
│  │         ChromaDB (vector_db.py)             │  │
│  │   - Vector storage for reports               │  │
│  │   - Semantic search                          │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 📡 API Endpoint Mapping

### Company Profile

| Frontend Hook | Backend Endpoint | Method | Description |
|--------------|------------------|--------|-------------|
| `useCompanyProfile()` | `/api/profile` | GET | Get company profile |
| `profile.updateProfile()` | `/api/profile` | PUT | Update company profile |

### Reports

| Frontend Hook | Backend Endpoint | Method | Description |
|--------------|------------------|--------|-------------|
| `useReports()` | `/api/reports?limit=50&offset=0` | GET | List all reports with pagination |
| `useReport(id)` | `/api/reports/{report_id}` | GET | Get specific report by ID |
| `useGenerateReport()` | `/api/reports/generate` | POST | Generate new compliance report |
| `useDeleteReport()` | `/api/reports/{report_id}` | DELETE | Delete a report |
| `useSearchReports()` | `/api/reports/search?q={query}` | GET | Semantic search for reports |

### PDF Operations

| Frontend Hook | Backend Endpoint | Method | Description |
|--------------|------------------|--------|-------------|
| `useDownloadPDF()` | `/api/reports/{report_id}/pdf` | GET | Download PDF report |
| `api.getPDFInfo()` | `/api/reports/{report_id}/pdf/info` | GET | Get PDF metadata |
| `api.searchPDFs()` | `/api/reports/pdfs/search?q={query}` | GET | Search PDFs semantically |

### Chat

| Frontend Hook | Backend Endpoint | Method | Description |
|--------------|------------------|--------|-------------|
| `useChat(reportId)` | `/api/chat/{report_id}/history` | GET | Get chat history |
| `chat.sendMessage()` | `/api/chat/{report_id}/message` | POST | Send chat message |
| `api.getSuggestedQuestions()` | `/api/chat/{report_id}/suggestions` | GET | Get suggested questions |
| `chat.clearHistory()` | `/api/chat/{report_id}/history` | DELETE | Clear chat history |
| `api.connectChatWebSocket()` | `/api/chat/{report_id}/ws` | WebSocket | Real-time chat connection |

### Utilities

| Frontend Hook | Backend Endpoint | Method | Description |
|--------------|------------------|--------|-------------|
| `useAppStats()` | `/api/stats` | GET | Get application statistics |
| `api.healthCheck()` | `/api/health` | GET | Health check endpoint |

---

## 🔑 Key Workflows

### 1. **Generate Report Workflow**

**Frontend Component:**
```tsx
import { useGenerateReport, useReports } from "@/lib/hooks/use-api"

function GenerateReportButton() {
  const { generate, loading, error, reportId } = useGenerateReport()
  const { refetch } = useReports()

  const handleGenerate = async () => {
    try {
      const result = await generate()
      console.log("Report generated:", result.report_id)

      // Refresh report list
      await refetch()

      // Navigate to new report
      router.push(`/report/${result.report_id}`)
    } catch (err) {
      console.error("Generation failed:", err)
    }
  }

  return (
    <button onClick={handleGenerate} disabled={loading}>
      {loading ? "Generating..." : "Generate Report"}
    </button>
  )
}
```

**Backend Flow:**
```
POST /api/reports/generate
  ↓
Load company profile from file
  ↓
ReportService.generate_report()
  ↓
SearchAgent → Search for compliance data
  ↓
ReportGeneratorAgent → Create structured report
  ↓
ValidatorAgent → Validate report quality (up to 3 iterations)
  ↓
PDFService → Generate PDF
  ↓
Save to ChromaDB
  ↓
Return report_id
```

**Expected Time:** 2-4 minutes (includes AI processing)

---

### 2. **List Reports Workflow**

**Frontend Component:**
```tsx
import { useReports } from "@/lib/hooks/use-api"

function ReportsList() {
  const { reports, total, loading, error } = useReports({ limit: 20, offset: 0 })

  if (loading) return <div>Loading reports...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div>
      <h2>Reports ({total})</h2>
      {reports.map(report => (
        <ReportCard key={report.id} report={report} />
      ))}
    </div>
  )
}
```

**Backend Flow:**
```
GET /api/reports?limit=20&offset=0
  ↓
ReportService.get_all_reports()
  ↓
Load all JSON files from data/reports/
  ↓
Apply pagination
  ↓
Return { reports: [...], total: N }
```

---

### 3. **View Report Details Workflow**

**Frontend Component:**
```tsx
import { useReport } from "@/lib/hooks/use-api"

function ReportDetailPage({ params }: { params: { id: string } }) {
  const { report, loading, error } = useReport(params.id)

  if (loading) return <div>Loading report...</div>
  if (error) return <div>Error: {error}</div>
  if (!report) return <div>Report not found</div>

  return (
    <div>
      <h1>{report.company_name} Compliance Report</h1>
      <ReportSummary summary={report.content.summary} />
      <LegalChanges changes={report.content.legal_changes} />
      <RouteImpacts impacts={report.content.route_impacts} />
      <RecommendedActions actions={report.content.recommended_actions} />
    </div>
  )
}
```

**Backend Flow:**
```
GET /api/reports/{report_id}
  ↓
ReportService.get_report_by_id(report_id)
  ↓
Load data/reports/{report_id}.json
  ↓
Return full report object
```

---

### 4. **Chat with Report Workflow**

**Frontend Component:**
```tsx
import { useChat } from "@/lib/hooks/use-api"

function ChatInterface({ reportId }: { reportId: string }) {
  const { messages, sendMessage, loading } = useChat(reportId)
  const [input, setInput] = useState("")

  const handleSend = async () => {
    await sendMessage(input)
    setInput("")
  }

  return (
    <div>
      <MessageList messages={messages} />
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        disabled={loading}
      />
      <button onClick={handleSend} disabled={loading}>Send</button>
    </div>
  )
}
```

**Backend Flow:**
```
POST /api/chat/{report_id}/message
  ↓
ChatService.send_message(report_id, message)
  ↓
ChatAgent → RAG search in ChromaDB
  ↓
Retrieve relevant report context
  ↓
Generate answer with Claude
  ↓
Save to chat history
  ↓
Return { message_id, content, sources }
```

---

### 5. **Download PDF Workflow**

**Frontend Component:**
```tsx
import { useDownloadPDF } from "@/lib/hooks/use-api"

function DownloadButton({ reportId }: { reportId: string }) {
  const { download, loading } = useDownloadPDF()

  return (
    <button
      onClick={() => download(reportId)}
      disabled={loading}
    >
      {loading ? "Downloading..." : "Download PDF"}
    </button>
  )
}
```

**Backend Flow:**
```
GET /api/reports/{report_id}/pdf
  ↓
Get PDF metadata from ChromaDB
  ↓
Check if PDF file exists
  ↓
Return FileResponse (application/pdf)
  ↓
Browser downloads file
```

---

## 🚀 Getting Started

### 1. **Start Backend** (Port 8000)

```bash
cd backend
python main.py
```

**Expected Output:**
```
============================================================
🚀 Logistics Compliance App v1.0.0
============================================================

📁 Initializing data directories...
🗄️  Initializing ChromaDB...
   ✓ ChromaDB initialized (5 reports in database)
✓ Company profile found at: ./data/company_profile.json

📋 Configuration:
   • Model: claude-sonnet-4-5
   • Data directory: ./data
   • ChromaDB path: ./data/chroma_data
   • Max validation iterations: 3

============================================================
✅ Application started successfully
📚 API Documentation: http://localhost:8000/docs
============================================================
```

### 2. **Start Frontend** (Port 3000)

```bash
cd v0-logistics-ai-reports-fx
npm install
npm run dev
```

**Expected Output:**
```
  ▲ Next.js 15.5.6
  - Local:        http://localhost:3000
  - Network:      http://192.168.1.100:3000

 ✓ Ready in 2.5s
```

### 3. **Verify Connection**

Open browser: http://localhost:3000

The frontend should:
- ✅ Load report list from backend
- ✅ Display company information
- ✅ Allow generating new reports
- ✅ Show report details
- ✅ Enable PDF downloads
- ✅ Support chat functionality

---

## 🔧 Configuration

### Frontend Configuration (`.env.local`)

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend Configuration (`.env`)

```bash
# Already configured with CORS enabled
ANTHROPIC_API_KEY=your_api_key_here
CLAUDE_MODEL=claude-sonnet-4-5
```

---

## 🐛 Troubleshooting

### Issue: "Failed to fetch"

**Symptoms:**
```
Error: Failed to fetch reports
Network request failed
```

**Solutions:**
1. **Check backend is running:**
   ```bash
   curl http://localhost:8000/api/health
   ```
   Should return: `{"status": "ok", "timestamp": "..."}`

2. **Check CORS is enabled:**
   Backend `main.py` should have:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. **Check frontend env:**
   File `.env.local` should have:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

### Issue: "Report generation takes too long"

**Expected:** 2-4 minutes (AI processing)

**If longer:**
1. Check backend console for errors
2. Check MCP configuration (if using real search)
3. Verify Claude API key is valid

### Issue: "PDF download fails"

**Solutions:**
1. Check if PDF was generated:
   ```bash
   curl http://localhost:8000/api/reports/{report_id}/pdf/info
   ```

2. Check PDF directory exists:
   ```bash
   ls backend/data/reports/pdfs/
   ```

3. Regenerate report if PDF is missing

---

## 📊 Data Flow Examples

### Example 1: Generate Report

**Frontend Request:**
```typescript
const result = await api.generateReport({})
```

**HTTP Request:**
```http
POST http://localhost:8000/api/reports/generate
Content-Type: application/json

{}
```

**Backend Response:**
```json
{
  "report_id": "abc-123-def",
  "status": "approved",
  "message": "Report generated successfully after 2 iteration(s)"
}
```

### Example 2: Get Report

**Frontend Request:**
```typescript
const report = await api.getReport("abc-123-def")
```

**HTTP Request:**
```http
GET http://localhost:8000/api/reports/abc-123-def
```

**Backend Response:**
```json
{
  "id": "abc-123-def",
  "company_name": "EuroTrans Logistics",
  "status": "approved",
  "content": {
    "summary": {
      "total_changes": 5,
      "overall_risk": "medium",
      "key_takeaways": [...]
    },
    "legal_changes": [...],
    "route_impacts": [...],
    "recommended_actions": [...]
  },
  "generated_at": "2025-01-18T10:30:00Z",
  "iteration_count": 2
}
```

---

## ✅ Integration Checklist

- [x] API client created (`lib/api.ts`)
- [x] TypeScript types defined (`lib/types.ts`)
- [x] React hooks created (`lib/hooks/use-api.ts`)
- [x] Environment configuration (`.env.local`)
- [x] CORS enabled in backend
- [x] Backend endpoints documented
- [x] Example usage provided

---

## 🎯 Next Steps

1. **Update main page** (`app/page.tsx`) to use `useReports()` hook
2. **Update report detail page** (`app/report/[id]/page.tsx`) to use `useReport()` hook
3. **Add generate report button** with `useGenerateReport()` hook
4. **Add chat interface** with `useChat()` hook
5. **Add PDF download button** with `useDownloadPDF()` hook
6. **Test all workflows** end-to-end

---

Your frontend is now ready to connect to the backend! 🚀
