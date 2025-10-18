"""
Search Agent - Generates targeted search queries and retrieves relevant data.
First agent in the pipeline.
"""

from anthropic import Anthropic
from config import settings
from mcp_client import get_mcp_client
from typing import List, Dict, Any
import json


class SearchAgent:
    """Agent responsible for searching and gathering compliance information."""

    def __init__(self):
        """Initialize Search Agent with Claude client."""
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.CLAUDE_MODEL
        self.mcp_client = get_mcp_client()

    async def execute(self, company_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute search agent to gather compliance data.

        Args:
            company_profile: Company profile data

        Returns:
            Dictionary with search results and metadata
        """
        print("🔍 Search Agent: Starting data gathering...")

        try:
            # Step 1: Generate search queries using Claude
            queries = await self._generate_search_queries(company_profile)
            print(f"   Generated {len(queries)} search queries")

            # Step 2: Execute searches via MCP
            search_results = await self._execute_searches(queries)
            print(f"   Retrieved {len(search_results)} search results")

            # Step 3: Filter and rank results
            filtered_results = await self._filter_results(
                search_results,
                company_profile
            )
            print(f"   Filtered to {len(filtered_results)} relevant results")

            return {
                "success": True,
                "search_results": filtered_results,
                "queries_used": queries,
                "total_results": len(search_results)
            }

        except Exception as e:
            print(f"❌ Search Agent error: {e}")
            return {
                "success": False,
                "error": str(e),
                "search_results": []
            }

    async def _generate_search_queries(
        self,
        company_profile: Dict[str, Any]
    ) -> List[str]:
        """Generate targeted search queries based on company profile."""

        prompt = f"""You are a logistics compliance research assistant. Generate targeted search queries to find recent legal and regulatory changes affecting this company.

Company Profile:
- Name: {company_profile.get('company_name')}
- Routes: {json.dumps(company_profile.get('routes', []), indent=2)}
- Fleet: {json.dumps(company_profile.get('fleet', []), indent=2)}
- Cargo Categories: {company_profile.get('cargo_categories', [])}

Generate 8-10 specific search queries that will help find:
1. Recent legal changes in the countries/routes they operate in
2. New regulations affecting their vehicle types
3. Cargo-specific compliance requirements
4. Border control updates
5. Emission standards and environmental regulations

Return ONLY a JSON array of search query strings, nothing else.
Example: ["query 1", "query 2", "query 3"]"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse queries from response
        content = response.content[0].text.strip()

        try:
            queries = json.loads(content)
            if isinstance(queries, list):
                return queries[:10]
        except json.JSONDecodeError:
            # Fallback: extract queries from text
            pass

        # Fallback queries based on profile
        fallback_queries = [
            f"logistics regulations {company_profile.get('company_name')} 2024",
            "EU transport law changes 2024",
            "cross-border cargo requirements Europe"
        ]

        return fallback_queries

    async def _execute_searches(self, queries: List[str]) -> List[Dict[str, str]]:
        """Execute all search queries via MCP client."""
        all_results = []

        for query in queries:
            try:
                results = await self.mcp_client.search_web(
                    query=query,
                    max_results=5
                )
                all_results.extend(results)
            except Exception as e:
                print(f"   Warning: Search failed for '{query}': {e}")
                continue

        # Deduplicate by URL
        seen_urls = set()
        unique_results = []
        for result in all_results:
            if result["url"] not in seen_urls:
                seen_urls.add(result["url"])
                unique_results.append(result)

        return unique_results

    async def _filter_results(
        self,
        search_results: List[Dict[str, str]],
        company_profile: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Filter and rank search results by relevance using Claude."""

        if len(search_results) <= 15:
            return search_results

        # Use Claude to rank results by relevance
        prompt = f"""You are filtering search results for a logistics company. Rank these results by relevance and return the top 15.

Company Profile:
{json.dumps(company_profile, indent=2)}

Search Results:
{json.dumps(search_results, indent=2)}

Return a JSON array of the top 15 most relevant result URLs in order of importance.
Format: ["url1", "url2", ...]"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text.strip()
            ranked_urls = json.loads(content)

            # Reorder results based on ranking
            url_to_result = {r["url"]: r for r in search_results}
            filtered = []
            for url in ranked_urls:
                if url in url_to_result:
                    filtered.append(url_to_result[url])

            return filtered[:15]

        except Exception:
            # Fallback: return first 15
            return search_results[:15]
