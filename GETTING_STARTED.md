# 🚀 Quick Start Guide - Logistics Compliance Backend

This is the backend application for the AI-powered Logistics Compliance monitoring system. This guide will help you set up and run the backend in **under 5 minutes**.

## 📋 Prerequisites

Before you begin, make sure you have:

- **Python 3.10 or higher** installed ([Download Python](https://www.python.org/downloads/))
- **Anthropic API Key** ([Get one here](https://console.anthropic.com/))
- Basic familiarity with terminal/command line

## 🏗️ Project Structure

```
Logistic_simple/
├── backend/                    # Backend application
│   ├── main.py                # FastAPI entry point
│   ├── config.py              # Configuration management
│   ├── routes.py              # API endpoints
│   ├── vector_db.py           # ChromaDB setup
│   ├── mcp_client.py          # MCP integration
│   ├── simplified_models.py   # Data models
│   ├── agents/                # AI agents
│   │   ├── search_agent.py
│   │   ├── report_agent.py
│   │   ├── validator_agent.py
│   │   └── chat_agent.py
│   ├── services/              # Business logic
│   │   ├── report_service.py
│   │   └── chat_service.py
│   ├── requirements.txt       # Python dependencies
│   └── .env.example          # Environment template
├── data/                      # Data storage (auto-created)
│   ├── company_profile.json  # Your company info
│   ├── reports/              # Generated reports
│   ├── chat_history/         # Chat conversations
│   └── chroma_data/          # Vector database
└── example_company.json      # Example company profile
```

## ⚡ Quick Setup (5 Steps)

### Step 1: Create Virtual Environment

Open terminal and navigate to the backend directory:

```bash
cd backend
python -m venv venv
```

**Activate the virtual environment:**

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

You should see `(venv)` in your terminal prompt.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- Anthropic SDK (Claude AI)
- ChromaDB (vector database)
- Pydantic (data validation)
- And other dependencies

### Step 3: Configure Environment

Create your `.env` file:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

**Edit `.env` and add your Anthropic API key:**

```bash
ANTHROPIC_API_KEY=your_actual_api_key_here
```

All other settings have sensible defaults and can be left as-is.

### Step 4: Create Company Profile

Copy the example company profile to the data directory:

```bash
# Windows
mkdir ..\data
copy ..\example_company.json ..\data\company_profile.json

# macOS/Linux
mkdir -p ../data
cp ../example_company.json ../data/company_profile.json
```

**Optional:** Edit `../data/company_profile.json` to match your actual company details.

### Step 5: Run the Backend

```bash
python main.py
```

You should see:

```
🚀 Logistics Compliance App v1.0.0
================================================================

📁 Initializing data directories...
🗄️  Initializing ChromaDB...
   ✓ ChromaDB initialized (0 reports in database)
✓ Company profile found at: ./data/company_profile.json

📋 Configuration:
   • Model: claude-3-5-sonnet-20241022
   • Data directory: ./data
   • ChromaDB path: ./data/chroma_data
   • Max validation iterations: 3
   ⚠️  MCP Server not configured (using mock data)

================================================================
✅ Application started successfully
📚 API Documentation: http://localhost:8000/docs
================================================================
```

**🎉 Your backend is now running on http://localhost:8000**

## 🧪 Testing the Backend

### 1. Check Health Status

Open your browser and visit:
```
http://localhost:8000/api/health
```

You should see:
```json
{
  "status": "ok",
  "timestamp": "2024-01-18T10:30:00.000000"
}
```

### 2. View API Documentation

Visit the auto-generated API docs:
```
http://localhost:8000/docs
```

This gives you an interactive interface to test all endpoints.

### 3. Get Company Profile

```bash
curl http://localhost:8000/api/profile
```

Or open in browser: http://localhost:8000/api/profile

### 4. Generate Your First Report

Using curl:
```bash
curl -X POST http://localhost:8000/api/reports/generate \
  -H "Content-Type: application/json" \
  -d '{"force_refresh": false}'
```

Using Python:
```python
import requests

response = requests.post("http://localhost:8000/api/reports/generate")
print(response.json())
```

Using the Swagger UI:
1. Go to http://localhost:8000/docs
2. Find `POST /api/reports/generate`
3. Click "Try it out"
4. Click "Execute"

**This will take 2-3 minutes** as the AI agents work through the pipeline:
- 🔍 Search Agent gathers compliance data
- 📝 Report Generator creates the report
- ✅ Validator checks quality (up to 3 iterations)

### 5. View Generated Reports

```bash
curl http://localhost:8000/api/reports
```

Or visit: http://localhost:8000/api/reports

### 6. Chat with a Report

First, get a report ID from the reports list, then:

```bash
curl -X POST http://localhost:8000/api/chat/{report_id}/message \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the main risks in this report?"}'
```

Replace `{report_id}` with an actual report ID.

## 📚 API Endpoints Reference

### Company Profile
- `GET /api/profile` - Get company profile
- `PUT /api/profile` - Update company profile

### Reports
- `POST /api/reports/generate` - Generate new report (takes 2-3 min)
- `GET /api/reports` - List all reports
- `GET /api/reports/{id}` - Get specific report
- `GET /api/reports/search?q=query` - Semantic search
- `DELETE /api/reports/{id}` - Delete report

### Chat (RAG-powered Q&A)
- `POST /api/chat/{report_id}/message` - Send message
- `GET /api/chat/{report_id}/history` - Get chat history
- `GET /api/chat/{report_id}/suggestions` - Get suggested questions
- `DELETE /api/chat/{report_id}/history` - Clear history
- `WS /api/chat/{report_id}/ws` - WebSocket for real-time chat

### Utility
- `GET /api/health` - Health check
- `GET /api/stats` - Application statistics
- `GET /docs` - Interactive API documentation
- `GET /redoc` - Alternative API documentation

## 🔧 Configuration Options

Edit `.env` file to customize:

### Required Settings
```bash
ANTHROPIC_API_KEY=your_key_here  # REQUIRED
```

### Optional Settings
```bash
# Use real MCP server instead of mock data
MCP_SERVER_URL=https://your-mcp-server.com
MCP_API_KEY=your_mcp_key

# Change AI model (default is Claude 3.5 Sonnet)
CLAUDE_MODEL=claude-3-5-sonnet-20241022

# Increase/decrease validation iterations (default: 3)
MAX_VALIDATION_ITERATIONS=3

# Enable debug mode for detailed logging
DEBUG=true

# Simple password protection (optional)
APP_PASSWORD=your_secret_password
```

## 🗄️ Data Storage

All data is stored locally in the `data/` directory:

```
data/
├── company_profile.json       # Your company information
├── reports/                   # JSON files for each report
│   ├── {uuid}.json
│   └── {uuid}.json
├── chat_history/              # Chat conversations
│   ├── {report_id}_chat.json
│   └── {report_id}_chat.json
└── chroma_data/               # ChromaDB vector database (auto-managed)
```

### ChromaDB Storage
- **Fully local** - No external database needed
- **Persistent** - Survives application restarts
- **Automatic** - Embeddings generated automatically
- **Free** - No usage limits or costs

## 🛠️ Development Tips

### Running with Auto-Reload

For development, use uvicorn with reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Changes to `.py` files will automatically reload the server.

### Viewing ChromaDB Contents

```python
import chromadb

client = chromadb.PersistentClient(path="./data/chroma_data")
reports = client.get_collection("reports")

print(f"Total reports: {reports.count()}")
print(reports.peek())  # View first few items
```

### Resetting the Database

To start fresh (⚠️ deletes all data):

```bash
rm -rf data/chroma_data data/reports data/chat_history
```

Then restart the application.

### Logs and Debugging

Enable debug mode in `.env`:
```bash
DEBUG=true
```

The application will print detailed logs to the console.

## ❓ Troubleshooting

### Issue: Module not found

**Solution:** Make sure you're in the virtual environment and dependencies are installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: ANTHROPIC_API_KEY not found

**Solution:** Check that `.env` file exists and contains your API key:
```bash
cat .env  # or type .env on Windows
```

### Issue: Port 8000 already in use

**Solution:** Either kill the process using port 8000, or run on a different port:
```bash
python main.py --port 8001
```

Or edit `main.py` and change the port in the `uvicorn.run()` call.

### Issue: ChromaDB persistence not working

**Solution:** Ensure the data directory has write permissions:
```bash
chmod -R 755 data/  # macOS/Linux
```

On Windows, check folder permissions in Properties.

### Issue: MCP connection failed

This is **expected** if you haven't configured an MCP server. The app will use mock data instead, which is fine for development and testing.

To use real web search:
1. Get access to an MCP server (like ACI.dev)
2. Add credentials to `.env`:
   ```bash
   MCP_SERVER_URL=https://your-server.com
   MCP_API_KEY=your_key
   ```

## 🚀 Next Steps

1. **Test the API** - Use the Swagger UI at http://localhost:8000/docs
2. **Generate a report** - Try the report generation endpoint
3. **Chat with reports** - Test the RAG-powered chat feature
4. **Customize company profile** - Edit `data/company_profile.json` with your real data
5. **Build a frontend** - Connect a Next.js or React frontend to these APIs
6. **Add scheduling** - Set up automatic report generation (see specification)

## 📖 Additional Documentation

- **Full Specification**: See `specification.md` for complete architecture details
- **Data Models**: See `simplified_models.py` for all data structures
- **API Docs**: Visit http://localhost:8000/docs when running

## 💡 Tips for Success

1. **Start with mock data** - The app works great without MCP server
2. **Test endpoints individually** - Use the Swagger UI to experiment
3. **Check logs** - Console output shows detailed progress
4. **Be patient** - Report generation takes 2-3 minutes (it's doing a lot!)
5. **Customize company profile** - More specific data = better reports

## 🎯 Common Use Cases

### Daily Compliance Monitoring
```python
# Generate report automatically
import requests
response = requests.post("http://localhost:8000/api/reports/generate")
report_id = response.json()["report_id"]
print(f"New report: {report_id}")
```

### Search Past Reports
```python
# Find reports about specific topics
import requests
response = requests.get(
    "http://localhost:8000/api/reports/search",
    params={"q": "border control changes"}
)
print(response.json())
```

### Interactive Q&A
```python
# Chat about a report
import requests
response = requests.post(
    f"http://localhost:8000/api/chat/{report_id}/message",
    json={"message": "What should I do first?"}
)
print(response.json()["content"])
```

## 🆘 Getting Help

- **Check logs** - Most issues show helpful error messages
- **Test with curl** - Isolate if it's an API or client issue
- **Review specification.md** - Detailed architecture documentation
- **Check API docs** - http://localhost:8000/docs has examples

---

**Ready to go? Run `python main.py` and start monitoring compliance! 🚀**
