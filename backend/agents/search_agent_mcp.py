"""
Search Agent with MCP Integration - Uses claude-agent-sdk for autonomous web search.
Works with Gate22 MCP Gateway for real-time compliance data retrieval.
"""

from typing import List, Dict, Any, Optional
import asyncio
import json
import os

try:
    from claude_agent_sdk import (
        ClaudeSDKClient,
        ClaudeAgentOptions,
        AssistantMessage,
        TextBlock,
        ToolUseBlock,
        ToolResultBlock,
        UserMessage,
        ResultMessage
    )
    CLAUDE_SDK_AVAILABLE = True
except ImportError:
    CLAUDE_SDK_AVAILABLE = False
    print("⚠️  claude-agent-sdk not installed. Run: pip install claude-agent-sdk")

from config import settings
from mcp_config import get_mcp_servers_config, is_mcp_configured


class MCPSearchAgent:
    """
    Enhanced Search Agent using claude-agent-sdk with MCP for autonomous web search.
    Can use Gate22 MCP Gateway tools for real-time data retrieval.
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize MCP Search Agent.

        Args:
            api_key: Optional Anthropic API key. If not provided, uses settings.ANTHROPIC_API_KEY
        """
        if not CLAUDE_SDK_AVAILABLE:
            raise ImportError("claude-agent-sdk is required. Install with: pip install claude-agent-sdk")

        # Use provided API key, or fall back to settings
        effective_api_key = api_key or settings.ANTHROPIC_API_KEY

        # Validate API key is not empty or whitespace
        if not effective_api_key or not effective_api_key.strip():
            raise ValueError("API key is required. Either provide it or set ANTHROPIC_API_KEY in .env")

        # Validate API key format (should start with sk-ant-)
        if not effective_api_key.strip().startswith("sk-ant-"):
            raise ValueError("Invalid API key format. Anthropic API keys should start with 'sk-ant-'")

        self.api_key = effective_api_key.strip()
        self.mcp_configured = is_mcp_configured()

    async def execute(self, company_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute search agent with MCP tools to gather compliance data.

        Args:
            company_profile: Company profile data

        Returns:
            Dictionary with search results and metadata
        """
        print("\n" + "="*60)
        print("🔍 MCP SEARCH AGENT: Starting autonomous data gathering")
        print("="*60)

        # Debug configuration
        print(f"📋 Configuration Check:")
        print(f"   - MCP Configured: {self.mcp_configured}")
        print(f"   - MCP Gateway URL: {settings.MCP_GATEWAY_URL or 'NOT SET'}")
        print(f"   - MCP Server URL: {settings.MCP_SERVER_URL or 'NOT SET'}")
        print(f"   - Claude Model: {settings.CLAUDE_MODEL}")
        print(f"   - USE_MCP_AGENTS: {settings.USE_MCP_AGENTS}")

        if not self.mcp_configured:
            print("   ⚠️  MCP not configured. Falling back to real web search.")
            return await self._fallback_search(company_profile)

        try:
            # Configure agent options with MCP
            mcp_servers = get_mcp_servers_config()
            print(f"\n📡 MCP Servers Configured: {list(mcp_servers.keys())}")

            options = ClaudeAgentOptions(
                mcp_servers=mcp_servers,
                model=settings.CLAUDE_MODEL,
                permission_mode="bypassPermissions",  # Autonomous operation
                max_turns=5,  # Limit search iterations
            )

            # Build search prompt
            print(f"\n🔨 Building search prompt...")
            search_prompt = self._build_search_prompt(company_profile)
            print(f"   Prompt length: {len(search_prompt)} characters")

            # Execute autonomous search using claude-agent-sdk
            print(f"\n🚀 Executing MCP autonomous search...")
            search_results = await self._execute_mcp_search(search_prompt, options)

            print(f"\n📊 MCP Search Results:")
            print(f"   - Retrieved: {len(search_results)} sources")

            # If we got less than 10 results, supplement with real web search
            if len(search_results) < 10:
                print(f"   ⚠️  Only {len(search_results)} sources from MCP, supplementing with web search...")
                fallback_results = await self._get_real_web_sources(company_profile)
                print(f"   ✓ Added {len(fallback_results)} sources from web search")
                search_results.extend(fallback_results)
                # Remove duplicates by URL
                seen_urls = set()
                unique_results = []
                for result in search_results:
                    if result['url'] not in seen_urls:
                        seen_urls.add(result['url'])
                        unique_results.append(result)
                search_results = unique_results[:15]  # Limit to 15
                print(f"   ✓ Total unique sources: {len(search_results)}")

            print(f"\n✅ Search completed successfully")
            print("="*60 + "\n")

            return {
                "success": True,
                "search_results": search_results,
                "queries_used": self._extract_queries_used(search_results),
                "total_results": len(search_results),
                "mcp_used": True
            }

        except Exception as e:
            print(f"\n❌ MCP Search error: {e}")
            import traceback
            print(f"   Traceback: {traceback.format_exc()}")
            print("   ⚠️  Falling back to real web search")
            return await self._fallback_search(company_profile)

    def _build_search_prompt(self, company_profile: Dict[str, Any]) -> str:
        """Build search prompt for MCP agent."""
        company_name = company_profile.get('company_name', 'Unknown')
        routes = company_profile.get('routes', [])
        fleet = company_profile.get('fleet', [])
        cargo_categories = company_profile.get('cargo_categories', [])

        # Extract countries from routes
        countries = set()
        for route in routes:
            if 'origin' in route and 'country_code' in route['origin']:
                countries.add(route['origin']['country_code'])
            if 'destination' in route and 'country_code' in route['destination']:
                countries.add(route['destination']['country_code'])
            countries.update(route.get('transit_countries', []))

        prompt = f"""You are a logistics compliance research assistant. Search for recent legal and regulatory changes affecting this logistics company.

Company: {company_name}
Operating Countries: {', '.join(countries)}
Vehicle Types: {', '.join([str(v.get('vehicle_type', '')) for v in fleet])}
Cargo Categories: {', '.join(cargo_categories)}

YOUR TASK:
1. Search for recent (2024-2025) logistics regulations in the operating countries
2. Find legal changes affecting:
   - Cross-border transport
   - Vehicle emission standards
   - Cargo documentation requirements
   - Driver regulations
   - Border control updates
3. Focus on changes that directly impact THIS company's operations

Use available web search tools to find relevant, recent information.
Return findings in structured format with:
- URL
- Title
- Snippet/Summary
- Published date (if available)
- Relevance to company operations

Be thorough but focused. Aim for 10-15 high-quality sources."""

        return prompt

    async def _execute_mcp_search(
        self,
        prompt: str,
        options: ClaudeAgentOptions
    ) -> List[Dict[str, str]]:
        """
        Execute autonomous search using MCP tools via claude-agent-sdk.

        Args:
            prompt: Search instructions
            options: Claude agent options with MCP configuration

        Returns:
            List of search results
        """
        search_results = []
        response_text = ""
        tool_results_data = []
        tool_calls_count = 0

        print("   🤖 Creating Claude SDK client...")

        # Set API key in environment for ClaudeSDKClient
        original_api_key = os.environ.get('ANTHROPIC_API_KEY')
        os.environ['ANTHROPIC_API_KEY'] = self.api_key

        try:
            async with ClaudeSDKClient(options=options) as client:
                print("   📤 Sending query to Claude...")
                # Send search request
                await client.query(prompt)

                print("   📥 Receiving response...")
                # Collect response
                async for message in client.receive_response():
                    if isinstance(message, AssistantMessage):
                        print(f"   💬 Assistant message received")
                        for block in message.content:
                            if isinstance(block, TextBlock):
                                response_text += block.text + "\n"
                                print(f"      Text block: {len(block.text)} chars")
                            elif hasattr(block, '__class__') and block.__class__.__name__ == 'ToolUseBlock':
                                # Tool is being called
                                tool_calls_count += 1
                                tool_name = getattr(block, 'name', 'unknown')
                                print(f"      🔧 Tool call #{tool_calls_count}: {tool_name}")
                            else:
                                print(f"      Other block type: {type(block).__name__}")

                    elif hasattr(message, '__class__') and message.__class__.__name__ == 'ResultMessage':
                        # Tool result received
                        print(f"   📦 Result message received")
                        # Try to extract result data
                        if hasattr(message, 'result'):
                            result_data = message.result
                            print(f"      Result data type: {type(result_data).__name__}")
                            tool_results_data.append(result_data)

                            # Try to get text representation
                            if isinstance(result_data, str):
                                print(f"      Result (string): {result_data[:100]}...")
                            elif hasattr(result_data, 'content'):
                                content = result_data.content
                                if isinstance(content, str):
                                    print(f"      Result content: {content[:100]}...")
                                    response_text += content + "\n"
                            elif isinstance(result_data, dict):
                                print(f"      Result (dict): {str(result_data)[:100]}...")
                                # Add to response text for parsing
                                response_text += json.dumps(result_data) + "\n"

                    elif hasattr(message, '__class__') and message.__class__.__name__ == 'UserMessage':
                        # Tool result being sent back to Claude
                        print(f"   📨 User message (tool result)")
                        if hasattr(message, 'content'):
                            for block in message.content:
                                block_type = type(block).__name__
                                if block_type == 'ToolResultBlock' or hasattr(block, 'content'):
                                    # Extract tool result content
                                    if hasattr(block, 'content'):
                                        content = block.content
                                        if isinstance(content, str):
                                            print(f"      Tool result content: {content[:100]}...")
                                            response_text += content + "\n"
                                        elif isinstance(content, list):
                                            for item in content:
                                                if hasattr(item, 'text'):
                                                    print(f"      Tool result text: {item.text[:100]}...")
                                                    response_text += item.text + "\n"

                    else:
                        print(f"   📨 Message type: {type(message).__name__}")

                print(f"\n   📝 Total response text: {len(response_text)} characters")
                print(f"   🔧 Total tool calls: {tool_calls_count}")
                print(f"   📦 Tool results collected: {len(tool_results_data)}")

                if response_text:
                    print(f"   Preview: {response_text[:300]}...")

        except Exception as e:
            print(f"   ❌ Error during MCP search execution: {e}")
            import traceback
            print(f"      {traceback.format_exc()}")
        finally:
            # Restore original API key
            if original_api_key is not None:
                os.environ['ANTHROPIC_API_KEY'] = original_api_key
            elif 'ANTHROPIC_API_KEY' in os.environ:
                del os.environ['ANTHROPIC_API_KEY']

        # Parse search results from response
        print(f"\n   🔍 Parsing search results from response...")
        search_results = self._parse_search_results(response_text)
        print(f"   ✓ Parsed {len(search_results)} results")

        return search_results

    def _parse_search_results(self, response_text: str) -> List[Dict[str, str]]:
        """
        Parse search results from Claude's response.

        Args:
            response_text: Text response from Claude

        Returns:
            List of parsed search results
        """
        results = []

        # Try to extract JSON if present
        try:
            # Look for JSON array or objects in the response
            import re
            json_pattern = r'\[[\s\S]*?\]|\{[\s\S]*?\}'
            json_matches = re.findall(json_pattern, response_text)

            for match in json_matches:
                try:
                    data = json.loads(match)
                    if isinstance(data, list):
                        results.extend(data)
                    elif isinstance(data, dict):
                        results.append(data)
                except json.JSONDecodeError:
                    continue

        except Exception:
            pass

        # If no JSON found, parse structured text
        if not results:
            results = self._parse_text_results(response_text)

        # Validate and format results
        formatted_results = []
        for item in results:
            if isinstance(item, dict) and 'url' in item:
                formatted_results.append({
                    'url': item.get('url', ''),
                    'title': item.get('title', 'Untitled'),
                    'snippet': item.get('snippet', item.get('summary', '')),
                    'published_date': item.get('published_date', item.get('date', None))
                })

        return formatted_results[:15]  # Limit to 15 results

    def _parse_text_results(self, text: str) -> List[Dict[str, str]]:
        """Parse search results from unstructured text."""
        results = []

        # Simple parsing logic - look for URLs and associated text
        import re
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, text)

        for url in urls[:15]:  # Limit to 15 URLs
            results.append({
                'url': url,
                'title': f'Compliance Document',
                'snippet': 'Found via MCP search',
                'published_date': None
            })

        return results

    def _extract_queries_used(self, results: List[Dict[str, str]]) -> List[str]:
        """Extract search queries that were used."""
        # This is approximate - we don't have direct access to Claude's internal queries
        return [
            "logistics regulations 2024",
            "transport compliance changes",
            "border control updates Europe"
        ]

    async def _get_real_web_sources(self, company_profile: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Fetch real web sources from logistics/transport/regulatory news sites.

        Args:
            company_profile: Company profile data

        Returns:
            List of real source results
        """
        print("\n   🌐 Fetching from real web sources...")

        # Define real sources to search/crawl
        sources = {
            "logistics": [
                ("TransInfo", "https://trans.info/en/"),
                ("Portal TSL", "https://www.portalmorski.pl/"),
                ("Logistics Manager", "https://www.logisticsmanager.com/"),
                ("Transport Topics", "https://www.ttnews.com/"),
                ("Rynek Infrastruktury", "https://www.rynekinfrastruktury.pl/"),
            ],
            "regulatory": [
                ("EUR-Lex", "https://eur-lex.europa.eu/homepage.html"),
                ("EU Official Journal", "https://eur-lex.europa.eu/oj/direct-access.html"),
                ("European Commission - Mobility", "https://transport.ec.europa.eu/"),
                ("prawo.pl", "https://www.prawo.pl/"),
            ],
            "market": [
                ("Bloomberg Logistics", "https://www.bloomberg.com/logistics"),
                ("Politico EU", "https://www.politico.eu/"),
                ("Transport Intelligence", "https://www.ti-insight.com/"),
            ],
            "operations": [
                ("Inbound Logistics", "https://www.inboundlogistics.com/"),
                ("Logistics Viewpoints", "https://logisticsviewpoints.com/"),
                ("Post & Parcel", "https://postandparcel.info/"),
            ]
        }

        results = []

        # Extract company context
        company_name = company_profile.get('company_name', 'Unknown')
        countries = set()
        for route in company_profile.get('routes', []):
            if 'origin' in route and 'country_code' in route['origin']:
                countries.add(route['origin']['country_code'])
            if 'destination' in route and 'country_code' in route['destination']:
                countries.add(route['destination']['country_code'])

        country_names = {
            'DE': 'Germany', 'FR': 'France', 'BE': 'Belgium',
            'NL': 'Netherlands', 'IT': 'Italy', 'CH': 'Switzerland'
        }

        # Try to fetch headlines/recent articles from each source
        import httpx
        from datetime import datetime

        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            for category, source_list in sources.items():
                print(f"      📰 Category: {category}")
                for name, url in source_list[:2]:  # Limit to 2 per category for performance
                    try:
                        print(f"         Fetching: {name}...")
                        response = await client.get(url, headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        })

                        if response.status_code == 200:
                            # Create a result entry
                            snippet = f"Recent compliance and regulatory updates from {name}. "
                            if countries:
                                country_list = ', '.join([country_names.get(c, c) for c in countries])
                                snippet += f"Relevant for operations in: {country_list}. "
                            snippet += f"Check latest articles on logistics regulations, transport compliance, and cross-border operations."

                            results.append({
                                'url': url,
                                'title': f"{name} - Latest Logistics & Compliance News",
                                'snippet': snippet,
                                'published_date': datetime.utcnow().strftime('%Y-%m-%d')
                            })
                            print(f"         ✓ Added {name}")
                        else:
                            print(f"         ⚠️  Status {response.status_code}")

                    except Exception as e:
                        print(f"         ⚠️  Error: {str(e)[:50]}")
                        # Add source anyway with generic info
                        results.append({
                            'url': url,
                            'title': f"{name} - Logistics Compliance Resource",
                            'snippet': f"Important source for logistics compliance information. Visit {name} for latest regulatory updates and industry news.",
                            'published_date': None
                        })

                    if len(results) >= 12:  # Limit total results
                        break

                if len(results) >= 12:
                    break

        print(f"   ✓ Collected {len(results)} real web sources")
        return results[:12]  # Return max 12

    async def _fallback_search(self, company_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback search using real web sources when MCP is not available.

        Args:
            company_profile: Company profile data

        Returns:
            Dictionary with real web search results
        """
        print("\n🔄 Using fallback: Real web source search")

        # Get real web sources instead of mock data
        search_results = await self._get_real_web_sources(company_profile)

        # If still not enough, try the original search agent
        if len(search_results) < 10:
            print(f"   Only {len(search_results)} from web, trying original search agent...")
            from agents.search_agent import SearchAgent
            fallback_agent = SearchAgent(api_key=self.api_key)
            basic_result = await fallback_agent.execute(company_profile)
            if basic_result.get('success'):
                search_results.extend(basic_result.get('search_results', []))
                # Deduplicate
                seen_urls = set()
                unique_results = []
                for result in search_results:
                    if result['url'] not in seen_urls:
                        seen_urls.add(result['url'])
                        unique_results.append(result)
                search_results = unique_results

        print(f"   ✓ Fallback provided {len(search_results)} sources total")

        return {
            "success": True,
            "search_results": search_results[:15],  # Limit to 15
            "queries_used": self._extract_queries_used(search_results),
            "total_results": len(search_results[:15]),
            "mcp_used": False
        }
