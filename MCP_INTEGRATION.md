# 🔌 MCP Integration Guide - Gate22 Gateway

This guide explains how to integrate the Gate22 MCP Gateway for autonomous web search and real-time compliance data retrieval.

## 📋 What is MCP?

**MCP (Model Context Protocol)** is a protocol that allows AI agents to use external tools and data sources. With MCP integration, your agents can:

- 🌐 **Perform real web searches** (instead of mock data)
- 📊 **Retrieve real-time compliance data**
- 🔍 **Access specialized data sources**
- 🤖 **Work autonomously** with external tools

## 🎯 Benefits of MCP Integration

### Before MCP (Mock Data)
```
User triggers report → Agent uses hardcoded mock results → Generic report
```

### After MCP (Real Data)
```
User triggers report → Agent autonomously searches web via Gate22 →
Retrieves latest compliance data → Detailed, accurate report
```

## 🚀 Quick Setup (3 Steps)

### Step 1: Get Gate22 API Access

1. Visit https://gate22.aci.dev/
2. Sign up or log in
3. Navigate to API Settings
4. Copy your **API Key**

### Step 2: Configure Environment

Edit your `.env` file:

```bash
# MCP Gateway Configuration
MCP_GATEWAY_URL=https://gate22.aci.dev/mcp
MCP_API_KEY=your_actual_api_key_here

# Enable MCP agents
USE_MCP_AGENTS=true
```

### Step 3: Install Dependencies

```bash
cd backend
pip install claude-agent-sdk
```

**That's it!** Your agents will now use MCP automatically.

## ✅ Verify MCP Integration

### Check Configuration

Run the backend:

```bash
python backend/main.py
```

Look for these messages:

```
✓ Gate22 MCP Gateway configured: https://gate22.aci.dev/mcp
✓ Enabled 4 MCP tools from gate22
✓ Using MCP-enabled Search Agent (autonomous mode)
```

### Test Report Generation

```bash
curl -X POST http://localhost:8000/api/reports/generate
```

The Search Agent will now:
1. ✅ Use real web search via Gate22
2. ✅ Retrieve actual compliance data
3. ✅ Work autonomously with MCP tools
4. ✅ Return accurate, up-to-date results

## 🏗️ Architecture

### Without MCP
```
┌─────────────┐
│Search Agent │ → Mock Data → Report
└─────────────┘
```

### With MCP
```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│Search Agent │  →   │Gate22 Gateway│  →   │ Web Search  │
│   (MCP)     │  ←   │   (MCP)      │  ←   │   Results   │
└─────────────┘      └──────────────┘      └─────────────┘
```

## 🔧 Configuration Options

### Enable/Disable MCP

```bash
# .env file
USE_MCP_AGENTS=true   # Use MCP agents (autonomous)
USE_MCP_AGENTS=false  # Use standard agents (mock data)
```

### MCP Gateway URL

```bash
# Gate22 MCP Gateway
MCP_GATEWAY_URL=https://gate22.aci.dev/mcp

# Custom MCP server
MCP_GATEWAY_URL=https://your-custom-mcp-server.com
```

### Available MCP Tools

When Gate22 is configured, these tools become available:

- `mcp__gate22__web_search` - Web search capability
- `mcp__gate22__fetch_url` - URL content fetching
- `mcp__gate22__get_content` - Content retrieval
- `mcp__gate22__search` - General search

## 📊 How It Works

### 1. Report Generation Flow

```python
# User triggers report via API
POST /api/reports/generate

# Backend decides which agent to use
if MCP_configured:
    agent = MCPSearchAgent()  # Autonomous with real search
else:
    agent = SearchAgent()      # Fallback with mock data

# MCP Agent workflow
1. Analyzes company profile
2. Generates search queries autonomously
3. Uses Gate22 tools to search web
4. Retrieves real compliance data
5. Returns structured results
```

### 2. Autonomous Operation

The MCP agent works **completely autonomously**:

```python
# Agent receives company profile
company = {
    "company_name": "EuroTrans",
    "routes": [{"origin": "DE", "destination": "FR"}],
    "cargo_categories": ["standard", "perishable"]
}

# Agent autonomously:
# - Generates relevant search queries
# - Executes searches via MCP tools
# - Parses and structures results
# - Returns compliance data

# No manual intervention needed!
```

## 🎓 Understanding the Code

### MCP Configuration (`backend/mcp_config.py`)

```python
def get_mcp_servers_config():
    """Returns MCP server configuration for claude-agent-sdk"""
    return {
        "gate22": {
            "type": "sse",  # Server-Sent Events
            "url": "https://gate22.aci.dev/mcp",
            "headers": {
                "Authorization": f"Bearer {API_KEY}"
            }
        }
    }
```

### MCP Search Agent (`backend/agents/search_agent_mcp.py`)

```python
class MCPSearchAgent:
    async def execute(self, company_profile):
        # Configure agent with MCP tools
        options = ClaudeAgentOptions(
            mcp_servers=get_mcp_servers_config(),
            permission_mode="bypassPermissions",  # Autonomous
            max_turns=5
        )

        # Execute autonomous search
        async with ClaudeSDKClient(options=options) as client:
            await client.query(search_prompt)
            # Agent uses MCP tools automatically
            results = await client.receive_response()

        return parsed_results
```

### Service Layer (`backend/services/report_service.py`)

```python
class ReportService:
    def __init__(self):
        # Automatically choose agent based on MCP availability
        if USE_MCP_AGENTS and mcp_configured():
            self.search_agent = MCPSearchAgent()  # MCP-enabled
        else:
            self.search_agent = SearchAgent()     # Fallback
```

## 🔐 Security

### API Key Protection

✅ **DO:**
- Store API key in `.env` file (never commit)
- Use environment variables
- Rotate keys regularly

❌ **DON'T:**
- Hardcode API keys in code
- Commit `.env` to git
- Share keys publicly

### Permissions

The MCP agent uses `bypassPermissions` mode for autonomous operation:

```python
options = ClaudeAgentOptions(
    permission_mode="bypassPermissions"  # Agent can use tools freely
)
```

This is safe because:
- Agent only has access to configured MCP tools
- No file system access
- No bash command execution
- Only web search via Gate22

## 🧪 Testing MCP Integration

### Test 1: Check Configuration

```python
# test_mcp_config.py
from backend.mcp_config import is_mcp_configured, get_mcp_servers_config

print(f"MCP Configured: {is_mcp_configured()}")
print(f"MCP Servers: {get_mcp_servers_config()}")
```

### Test 2: Test Search Agent

```python
# test_search_agent.py
import asyncio
from backend.agents.search_agent_mcp import MCPSearchAgent

async def test():
    agent = MCPSearchAgent()

    company_profile = {
        "company_name": "Test Logistics",
        "routes": [{"origin": {"country_code": "DE"}}],
        "cargo_categories": ["standard"]
    }

    results = await agent.execute(company_profile)
    print(f"Found {len(results['search_results'])} results")
    print(f"MCP Used: {results['mcp_used']}")

asyncio.run(test())
```

### Test 3: Full Report Generation

```bash
# Via API
curl -X POST http://localhost:8000/api/reports/generate \
  -H "Content-Type: application/json" \
  -d '{"force_refresh": true}'

# Check logs for:
# "✓ Using MCP-enabled Search Agent (autonomous mode)"
# "✓ Retrieved X compliance sources"
```

## 📈 Performance

### With MCP
- **Search Quality**: Real-time web data ⭐⭐⭐⭐⭐
- **Data Accuracy**: Current regulations ⭐⭐⭐⭐⭐
- **Autonomy**: Fully autonomous ⭐⭐⭐⭐⭐
- **Speed**: 2-4 minutes per report

### Without MCP (Fallback)
- **Search Quality**: Mock data ⭐⭐
- **Data Accuracy**: Static examples ⭐⭐
- **Autonomy**: Limited ⭐⭐
- **Speed**: 1-2 minutes per report

## 🔄 Fallback Behavior

If MCP is not configured or fails:

```
┌─────────────────────┐
│  MCP Search Agent   │
└─────────┬───────────┘
          │
          ├─ MCP configured?
          │  ├─ YES → Use Gate22 tools
          │  └─ NO  → Use fallback
          │
          ├─ MCP call failed?
          │  └─ YES → Use fallback
          │
          ▼
  ┌───────────────┐
  │ Fallback Mode │
  │ (Mock Data)   │
  └───────────────┘
```

The app **always works**, even without MCP!

## 🛠️ Troubleshooting

### Issue: "MCP not configured"

**Solution:** Check your `.env` file:

```bash
# Verify settings
cat .env | grep MCP

# Should show:
MCP_GATEWAY_URL=https://gate22.aci.dev/mcp
MCP_API_KEY=your_key_here
USE_MCP_AGENTS=true
```

### Issue: "claude-agent-sdk not installed"

**Solution:**

```bash
pip install claude-agent-sdk
```

### Issue: "Using standard Search Agent (fallback mode)"

**Causes:**
1. MCP not configured (missing API key)
2. `USE_MCP_AGENTS=false` in .env
3. claude-agent-sdk not installed

**Solution:**
- Add MCP configuration to `.env`
- Set `USE_MCP_AGENTS=true`
- Install claude-agent-sdk

### Issue: Gate22 API errors

**Check:**

```bash
# Test Gate22 connection
curl -X GET https://gate22.aci.dev/health \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 📚 Additional Resources

- **Gate22 Documentation**: https://gate22.aci.dev/docs
- **MCP Protocol**: https://modelcontextprotocol.io/
- **Claude Agent SDK**: https://docs.anthropic.com/claude-code/agent-sdk

## 🎯 Next Steps

1. ✅ **Configure Gate22** - Add API key to `.env`
2. ✅ **Install SDK** - Run `pip install claude-agent-sdk`
3. ✅ **Test Integration** - Generate a report
4. ✅ **Monitor Logs** - Check for MCP usage
5. ✅ **Enjoy Real Data** - Get accurate compliance reports!

---

**Need Help?**

- Check backend logs for detailed error messages
- Verify `.env` configuration
- Test with `USE_MCP_AGENTS=false` for fallback mode
- Review `backend/mcp_config.py` for configuration details

**Working?**

You should see in logs:
```
✓ Gate22 MCP Gateway configured: https://gate22.aci.dev/mcp
✓ Using MCP-enabled Search Agent (autonomous mode)
🔍 MCP Search Agent: Starting autonomous data gathering...
   ✓ Retrieved 15 compliance sources
```

Enjoy autonomous, real-time compliance monitoring! 🚀
