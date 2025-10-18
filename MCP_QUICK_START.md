# ⚡ MCP Integration - Quick Start Card

## 🎯 Goal
Enable autonomous agents with real-time web search via Gate22 MCP Gateway.

## 📋 Prerequisites
- ✅ Backend already implemented
- ✅ Python 3.10+
- ✅ Anthropic API key configured

## 🚀 3-Step Setup

### Step 1: Get Gate22 API Key
```
🌐 Visit: https://gate22.aci.dev/
📝 Sign up / Login
🔑 Copy your API key
```

### Step 2: Configure .env
```bash
# Open .env file and add:
MCP_GATEWAY_URL=https://gate22.aci.dev/mcp
MCP_API_KEY=paste_your_key_here
USE_MCP_AGENTS=true
```

### Step 3: Install SDK
```bash
pip install claude-agent-sdk
```

## ✅ Verify Setup

### Start Backend
```bash
python backend/main.py
```

### Look for These Messages
```
✓ Gate22 MCP Gateway configured: https://gate22.aci.dev/mcp
✓ Enabled 4 MCP tools from gate22
✓ Using MCP-enabled Search Agent (autonomous mode)
```

## 🧪 Test It

### Trigger Report Generation
```bash
curl -X POST http://localhost:8000/api/reports/generate \
  -H "Content-Type: application/json" \
  -d '{"force_refresh": false}'
```

### Expected Output (in logs)
```
🔍 MCP Search Agent: Starting autonomous data gathering...
   ✓ Retrieved 15 compliance sources
   (MCP tools used autonomously)
📝 Report Generator Agent: Creating report...
✅ Report approved
```

## 🎛️ Configuration

### Enable MCP (Default)
```bash
USE_MCP_AGENTS=true
```

### Disable MCP (Fallback to Mock Data)
```bash
USE_MCP_AGENTS=false
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `backend/mcp_config.py` | MCP configuration |
| `backend/agents/search_agent_mcp.py` | MCP-enabled agent |
| `backend/services/report_service.py` | Auto-selects agent |
| `.env` | Configuration values |

## 🔧 How It Works

```
API Call → Report Service → Checks MCP Config
                              ↓
                    MCP Configured?
                    ├─ YES → MCPSearchAgent (real search)
                    └─ NO  → SearchAgent (mock data)
                              ↓
                    Agent works autonomously
                              ↓
                    Report generated
```

## 🐛 Troubleshooting

### Not Using MCP?

**Check:**
```bash
# 1. Verify .env
cat .env | grep MCP

# Should show:
MCP_GATEWAY_URL=https://gate22.aci.dev/mcp
MCP_API_KEY=your_key_here
USE_MCP_AGENTS=true

# 2. Check SDK installed
pip show claude-agent-sdk

# 3. Restart backend
python backend/main.py
```

### MCP Errors?

**Don't worry!** Automatic fallback to mock data.

**To investigate:**
- Check Gate22 API key validity
- Review backend logs
- Test Gate22 connection:
  ```bash
  curl https://gate22.aci.dev/health \
    -H "Authorization: Bearer YOUR_KEY"
  ```

## 📊 What You Get

### With MCP Enabled ✨
- 🌐 Real-time web search
- 📈 Actual compliance data
- 🤖 Fully autonomous agents
- ⭐ Accurate reports

### Without MCP (Fallback) 🔄
- 📋 Mock data
- ⚡ Faster generation
- 🔧 Good for testing
- ✅ Always works

## 🎯 API Endpoints (No Change!)

Your existing API works the same:

```bash
# Generate report (triggers MCP automatically)
POST /api/reports/generate

# List reports
GET /api/reports

# Get specific report
GET /api/reports/{id}

# Chat with report
POST /api/chat/{report_id}/message
```

**MCP integration is transparent!** 🎉

## 📚 Full Documentation

- **Complete Guide**: `MCP_INTEGRATION.md` (600 lines)
- **Summary**: `MCP_INTEGRATION_SUMMARY.md` (500 lines)
- **This Card**: Quick reference

## 💡 Pro Tips

1. **Test First**: Start with `USE_MCP_AGENTS=false` to verify setup
2. **Enable MCP**: Set to `true` for real data
3. **Monitor Logs**: Watch for MCP status messages
4. **Fallback Works**: App always functions, even if MCP fails

## 🎉 Success!

When working correctly, you'll see:

```
✓ Gate22 MCP Gateway configured
✓ Using MCP-enabled Search Agent (autonomous mode)
🔍 MCP Search Agent: Starting autonomous data gathering...
   ✓ Retrieved 15 compliance sources
```

## ⚙️ Environment Variables Summary

```bash
# Required for MCP
MCP_GATEWAY_URL=https://gate22.aci.dev/mcp
MCP_API_KEY=your_gate22_api_key

# Control MCP usage
USE_MCP_AGENTS=true

# Already configured
ANTHROPIC_API_KEY=your_anthropic_key
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

## 🔗 Quick Links

- Gate22 Portal: https://gate22.aci.dev/
- Backend Health: http://localhost:8000/api/health
- API Docs: http://localhost:8000/docs
- Report Generation: `POST /api/reports/generate`

---

**That's it! Your agents now work autonomously with real-time data! 🚀**

**Questions?** See `MCP_INTEGRATION.md` for detailed guide.
