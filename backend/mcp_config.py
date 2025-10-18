"""
MCP (Model Context Protocol) Configuration for Gate22 Integration.
Sets up MCP servers for use with claude-agent-sdk.
"""

from typing import Dict, Any
from config import settings


def get_mcp_servers_config() -> Dict[str, Any]:
    """
    Get MCP server configuration for claude-agent-sdk.

    Returns:
        Dictionary of MCP server configurations compatible with ClaudeAgentOptions.
    """
    print("\n🔧 MCP Configuration:")
    print(f"   MCP_GATEWAY_URL: {settings.MCP_GATEWAY_URL or 'NOT SET'}")
    print(f"   MCP_SERVER_URL: {settings.MCP_SERVER_URL or 'NOT SET'}")
    print(f"   MCP_API_KEY: {'SET' if settings.MCP_API_KEY else 'NOT SET'}")

    mcp_servers = {}

    # Gate22 MCP Gateway Configuration
    if settings.MCP_GATEWAY_URL and settings.MCP_API_KEY:
        # Configure Gate22 as an SSE (Server-Sent Events) MCP server
        mcp_servers["gate22"] = {
            "type": "sse",
            "url": settings.MCP_GATEWAY_URL,
            "headers": {
                "Authorization": f"Bearer {settings.MCP_API_KEY}",
                "Content-Type": "application/json"
            }
        }
        print(f"   ✓ Gate22 MCP Gateway configured: {settings.MCP_GATEWAY_URL}")

    # Legacy MCP server support (if using old configuration)
    elif settings.MCP_SERVER_URL:
        if settings.MCP_SERVER_URL.startswith("http"):
            mcp_servers["legacy_mcp"] = {
                "type": "sse",
                "url": settings.MCP_SERVER_URL,
                "headers": {
                    "Authorization": f"Bearer {settings.MCP_API_KEY}" if settings.MCP_API_KEY else ""
                }
            }
            print(f"   ✓ Legacy MCP server configured: {settings.MCP_SERVER_URL[:50]}...")
            print(f"      Type: SSE")
            print(f"      Auth: {'Enabled' if settings.MCP_API_KEY else 'Disabled'}")

    if not mcp_servers:
        print("   ⚠️  No MCP servers configured. Agents will use fallback methods.")
        print("   💡 Set MCP_GATEWAY_URL or MCP_SERVER_URL in .env to enable MCP")

    return mcp_servers


def get_allowed_mcp_tools() -> list[str]:
    """
    Get list of allowed MCP tools based on configured servers.

    Returns:
        List of tool names in format: mcp__<server>__<tool>
    """
    allowed_tools = []

    if settings.MCP_GATEWAY_URL or settings.MCP_SERVER_URL:
        # Common Gate22 MCP tools for web search and data retrieval
        server_name = "gate22" if settings.MCP_GATEWAY_URL else "legacy_mcp"

        # Web search capabilities
        allowed_tools.extend([
            f"mcp__{server_name}__web_search",
            f"mcp__{server_name}__fetch_url",
            f"mcp__{server_name}__get_content",
            f"mcp__{server_name}__search",
        ])

        print(f"✓ Enabled {len(allowed_tools)} MCP tools from {server_name}")

    return allowed_tools


# Default agent options for MCP-enabled agents
def get_agent_options() -> Dict[str, Any]:
    """
    Get default ClaudeAgentOptions configuration for agents.

    Returns:
        Dictionary with agent configuration options.
    """
    return {
        "mcp_servers": get_mcp_servers_config(),
        "allowed_tools": get_allowed_mcp_tools(),
        "model": settings.CLAUDE_MODEL,
        "permission_mode": "bypassPermissions",  # Allow autonomous operation
        "max_turns": 10,  # Reasonable limit for agent autonomy
    }


def is_mcp_configured() -> bool:
    """
    Check if any MCP server is configured.

    Returns:
        True if MCP is configured, False otherwise.
    """
    return bool(settings.MCP_GATEWAY_URL or settings.MCP_SERVER_URL)
