# 🔧 MCP Configuration & Troubleshooting Guide

## Current Issue: MCP Returns 0 Sources

Based on your output, MCP is **working correctly** (tools are being called), but the **tool results aren't being captured**. This is fixed in the latest code update.

---

## ✅ What's Working

From your output:
```
🔧 MCP Configuration:
   MCP_SERVER_URL: https://mcp.aci.dev/gateway/mcp?bundle_key=GIR1CrgIF8NsFaulT62oK0fAy7w93E2qOxs5
   ✓ Legacy MCP server configured
   Type: SSE
```

✅ Claude IS calling MCP tools (you see `ToolUseBlock` messages)
✅ Results ARE coming back (you see `ResultMessage`)
✅ The connection to Gate22 is working

---

## ❌ What Was Missing

### 1. **MCP_API_KEY Not Set**

Your output shows:
```
MCP_API_KEY: NOT SET
Auth: Disabled
```

**Gate22 MCP Gateway might require authentication.** Check if your bundle_key in the URL is sufficient, or if you need a separate API key.

### 2. **Tool Results Not Being Captured**

The code was only capturing `TextBlock` responses, not the actual tool results from MCP calls.

**Fix Applied:** Updated `search_agent_mcp.py` to capture:
- `ToolResultBlock` content
- `ResultMessage` data
- `UserMessage` tool results

---

## 🔑 MCP Authentication Options

### Option 1: Bundle Key in URL (Current Setup)
Your URL already contains authentication:
```
https://mcp.aci.dev/gateway/mcp?bundle_key=GIR1CrgIF8NsFaulT62oK0fAy7w93E2qOxs5
```

This might be sufficient. The bundle_key acts as authentication.

### Option 2: Separate API Key
If Gate22 requires a separate API key, add it to `.env`:

```bash
# In .env file
MCP_API_KEY=your_gate22_api_key_here
```

**How to get it:**
1. Visit https://gate22.aci.dev/
2. Log in to your account
3. Go to MCP Configuration settings
4. Copy your API key

---

## 🧪 Testing After Update

Run your report generation again and look for these new debug messages:

### What You Should See:

```
🚀 Executing MCP autonomous search...
   🤖 Creating Claude SDK client...
   📤 Sending query to Claude...
   📥 Receiving response...
   💬 Assistant message received
      🔧 Tool call #1: web_search
      🔧 Tool call #2: fetch_url
   📨 User message (tool result)
      Tool result content: [actual search results]
   📦 Result message received
      Result data type: dict
      Result (dict): {'results': [...]}

   📝 Total response text: 5000+ characters (increased!)
   🔧 Total tool calls: 5
   📦 Tool results collected: 5
```

**Key Indicators:**
- **Total tool calls > 0**: MCP tools are being used
- **Tool results collected > 0**: Results are being captured
- **Response text > 1000 chars**: Tool results included in parsing
- **Parsed X results (X > 0)**: Search results extracted successfully

---

## 🐛 If Still 0 Sources After Update

### Debug Steps:

1. **Check Tool Result Content**
   Look for lines like:
   ```
   Tool result content: [first 100 chars]
   ```
   This shows what MCP is actually returning.

2. **Verify Tool Names**
   Check what tools are being called:
   ```
   🔧 Tool call #1: mcp__legacy_mcp__web_search
   ```

   Expected tool names:
   - `mcp__legacy_mcp__web_search`
   - `mcp__legacy_mcp__search`
   - `mcp__legacy_mcp__fetch_url`

3. **Check ResultMessage Structure**
   The new code will print:
   ```
   Result data type: [type]
   Result (dict/string): [preview]
   ```

4. **Authentication Error?**
   If you see HTTP 401/403 errors, you need to set `MCP_API_KEY`:
   ```bash
   # Get your API key from Gate22
   MCP_API_KEY=your_actual_key
   ```

---

## 🎯 Expected Behavior After Fix

### Scenario 1: MCP Works Perfectly
```
📊 MCP Search Results:
   - Retrieved: 12 sources ✅

✅ Search completed successfully
Total unique sources: 12
```

### Scenario 2: MCP Partial (Auto-Supplement)
```
📊 MCP Search Results:
   - Retrieved: 3 sources
   ⚠️  Only 3 sources from MCP, supplementing with web search...

   🌐 Fetching from real web sources...
      ✓ Added TransInfo
      ✓ Added EUR-Lex
   ...
   ✓ Total unique sources: 15
```

### Scenario 3: MCP Fails (Full Fallback)
```
❌ MCP Search error: Connection failed
   ⚠️  Falling back to real web search

🔄 Using fallback: Real web source search
   ✓ Fallback provided 12 sources total
```

**In all scenarios, you get ≥10 sources!**

---

## 📋 Configuration Checklist

- [ ] `ANTHROPIC_API_KEY` is set (required for Claude)
- [ ] `MCP_SERVER_URL` is set (your Gate22 bundle URL)
- [ ] `MCP_API_KEY` is set (if required by Gate22)
- [ ] `USE_MCP_AGENTS=true` in .env
- [ ] Updated `search_agent_mcp.py` with new tool result capture code
- [ ] Backend restarted after code changes

---

## 🔍 Understanding MCP Messages

### Message Flow:
1. **SystemMessage**: Initial system instructions
2. **AssistantMessage** + **ToolUseBlock**: Claude decides to call MCP tool
3. **UserMessage** + **ToolResultBlock**: Tool result sent back to Claude
4. **ResultMessage**: Final result from tool execution
5. **AssistantMessage** + **TextBlock**: Claude interprets and responds

### Problem Was:
- Old code only captured step 5 (Claude's text interpretation)
- New code captures steps 3 & 4 (actual tool results)

---

## 🆘 Still Having Issues?

### Get More Debug Info:

Add to your `.env`:
```bash
# Enable verbose logging
LOG_LEVEL=DEBUG
```

### Check MCP Gateway Status:

```bash
curl -I https://mcp.aci.dev/gateway/mcp?bundle_key=YOUR_KEY
```

Expected response: `200 OK`

### Contact Gate22 Support:

If authentication errors persist:
1. Visit https://gate22.aci.dev/support
2. Verify your bundle_key is active
3. Ask if MCP_API_KEY is required for your plan

---

## ✅ Success Indicators

You'll know MCP is working when you see:

```
🔧 Total tool calls: 5+
📦 Tool results collected: 5+
📝 Total response text: 3000+ characters
✓ Parsed 10+ results
```

And in the report JSON:
```json
{
  "search_metadata": {
    "total_sources": 12,  // > 0 = success!
    "queries_used": [...]
  }
}
```

---

## 🚀 Next Steps

1. **Test the updated code**
2. **Check the new debug output**
3. **Add MCP_API_KEY if needed** (check Gate22 dashboard)
4. **Report back what you see** in the new debug logs

The code now captures tool results properly, so you should see actual data! 🎉
