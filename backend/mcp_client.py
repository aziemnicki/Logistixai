"""
MCP (Model Context Protocol) Client for web search integration.
Connects to ACI.dev or other MCP servers for real-time data retrieval.
"""

import httpx
from typing import List, Dict, Any, Optional
from config import settings
import asyncio


class MCPClient:
    """Client for interacting with MCP servers (e.g., ACI.dev)."""

    def __init__(self):
        """Initialize MCP client."""
        self.server_url = settings.MCP_SERVER_URL
        self.api_key = settings.MCP_API_KEY
        self.timeout = 30.0

    async def search_web(
        self,
        query: str,
        max_results: int = 10,
        region: Optional[str] = "eu"
    ) -> List[Dict[str, str]]:
        """
        Perform web search via MCP server.

        Args:
            query: Search query
            max_results: Maximum number of results
            region: Search region (eu, us, etc.)

        Returns:
            List of search results with url, title, snippet
        """
        # If MCP server is not configured, use mock data for development
        if not self.server_url:
            return self._mock_search(query, max_results)

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                headers = {}
                if self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"

                response = await client.post(
                    f"{self.server_url}/search",
                    json={
                        "query": query,
                        "max_results": max_results,
                        "region": region
                    },
                    headers=headers
                )
                response.raise_for_status()

                data = response.json()
                return data.get("results", [])

        except Exception as e:
            print(f"Error searching via MCP: {e}")
            # Fallback to mock data on error
            return self._mock_search(query, max_results)

    async def fetch_url_content(self, url: str) -> Optional[str]:
        """
        Fetch content from a URL via MCP server.

        Args:
            url: URL to fetch

        Returns:
            Page content as text
        """
        if not self.server_url:
            return None

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                headers = {}
                if self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"

                response = await client.post(
                    f"{self.server_url}/fetch",
                    json={"url": url},
                    headers=headers
                )
                response.raise_for_status()

                data = response.json()
                return data.get("content", "")

        except Exception as e:
            print(f"Error fetching URL via MCP: {e}")
            return None

    def _mock_search(self, query: str, max_results: int) -> List[Dict[str, str]]:
        """
        Mock search results for development/testing.

        This should be replaced with real MCP integration in production.
        """
        mock_results = [
            {
                "url": "https://example.com/eu-logistics-law-2024",
                "title": "New EU Logistics Regulations 2024",
                "snippet": "The European Union has introduced new logistics and transport regulations affecting cross-border cargo operations. Key changes include stricter emission standards and updated documentation requirements.",
                "published_date": "2024-01-15"
            },
            {
                "url": "https://example.com/border-control-updates",
                "title": "Border Control Updates for Transport Companies",
                "snippet": "Recent updates to border control procedures now require additional documentation for certain cargo categories. Companies operating in Belgium, France, and Germany should review their compliance procedures.",
                "published_date": "2024-02-01"
            },
            {
                "url": "https://example.com/emission-standards",
                "title": "Stricter Emission Standards for Heavy Vehicles",
                "snippet": "New emission standards will be enforced starting March 2024. All vehicles over 12 tons must comply with Euro 6d standards when operating in major European cities.",
                "published_date": "2024-01-20"
            },
            {
                "url": "https://example.com/cargo-documentation",
                "title": "Updated Cargo Documentation Requirements",
                "snippet": "Transport companies must now provide digital proof of cargo origin for all cross-border shipments. The new regulation applies to all EU member states and affects both standard and hazardous materials.",
                "published_date": "2024-02-10"
            },
            {
                "url": "https://example.com/driver-rest-periods",
                "title": "New Driver Rest Period Regulations",
                "snippet": "The EU has updated mandatory rest period regulations for professional drivers. New requirements include stricter monitoring and documentation of rest breaks during long-haul routes.",
                "published_date": "2024-01-25"
            }
        ]

        # Filter based on query keywords
        filtered = mock_results[:max_results]

        print(f"⚠️  Using mock search results for query: '{query}'")
        print(f"   Configure MCP_SERVER_URL in .env for real search")

        return filtered

    async def search_logistics_regulations(
        self,
        countries: List[str],
        cargo_categories: List[str],
        vehicle_types: List[str]
    ) -> List[Dict[str, str]]:
        """
        Specialized search for logistics regulations.

        Args:
            countries: List of country codes (DE, FR, BE, etc.)
            cargo_categories: Types of cargo (standard, hazardous, perishable)
            vehicle_types: Types of vehicles in fleet

        Returns:
            List of relevant search results
        """
        # Build targeted search queries
        queries = []

        # Country-specific regulations
        for country in countries:
            queries.append(f"logistics regulations {country} 2024")
            queries.append(f"transport law changes {country}")

        # Cargo-specific regulations
        for cargo in cargo_categories:
            queries.append(f"{cargo} cargo regulations Europe")

        # Vehicle-specific regulations
        for vehicle in vehicle_types:
            queries.append(f"{vehicle} regulations EU 2024")

        # Execute searches in parallel
        all_results = []
        for query in queries[:5]:  # Limit to avoid too many requests
            results = await self.search_web(query, max_results=5)
            all_results.extend(results)

        # Deduplicate by URL
        seen_urls = set()
        unique_results = []
        for result in all_results:
            if result["url"] not in seen_urls:
                seen_urls.add(result["url"])
                unique_results.append(result)

        return unique_results[:20]  # Return top 20 unique results


# Global MCP client instance
mcp_client = MCPClient()


def get_mcp_client() -> MCPClient:
    """Get the global MCP client instance."""
    return mcp_client
