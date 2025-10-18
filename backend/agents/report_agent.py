"""
Report Generator Agent - Creates structured compliance reports from search results.
Second agent in the pipeline.
"""

from anthropic import Anthropic
from config import settings
from typing import List, Dict, Any, Optional
import json


class ReportGeneratorAgent:
    """Agent responsible for generating structured compliance reports."""

    def __init__(self):
        """Initialize Report Generator Agent with Claude client."""
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.CLAUDE_MODEL

    async def execute(
        self,
        company_profile: Dict[str, Any],
        search_results: List[Dict[str, str]],
        previous_feedback: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a structured compliance report.

        Args:
            company_profile: Company profile data
            search_results: Search results from Search Agent
            previous_feedback: Feedback from Validator (for iterations)

        Returns:
            Dictionary with report content
        """
        print("📝 Report Generator Agent: Creating report...")

        try:
            report_content = await self._generate_report(
                company_profile,
                search_results,
                previous_feedback
            )

            print("   Report generated successfully")

            return {
                "success": True,
                "report": report_content
            }

        except Exception as e:
            print(f"❌ Report Generator error: {e}")
            return {
                "success": False,
                "error": str(e),
                "report": None
            }

    async def _generate_report(
        self,
        company_profile: Dict[str, Any],
        search_results: List[Dict[str, str]],
        previous_feedback: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate structured report using Claude."""

        feedback_section = ""
        if previous_feedback:
            feedback_section = f"""
IMPORTANT - Validator Feedback:
The previous version of this report was rejected with the following feedback:
{previous_feedback}

Please address these issues in this revised version.
"""

        prompt = f"""You are a logistics compliance analyst. Create a comprehensive compliance report with updates in the areas listed below:


<areas>
New transportation regulations (road, rail, sea, air)
- Customs and border control policy updates
- Environmental regulations affecting logistics (emissions standards, green zones)
- Labor laws impacting transportation workers
- Import/export restrictions and tariff changes
- Safety and compliance requirement updates
- Documentation and certification requirement changes




1. REGULATORY & LEGAL CHANGES
- New transportation regulations (road, rail, sea, air)
- Customs and border control policy updates
- Environmental regulations affecting logistics (emissions standards, green zones)
- Labor laws impacting transportation workers
- Import/export restrictions and tariff changes
- Safety and compliance requirement updates
- Documentation and certification requirement changes


2. GEOPOLITICAL EVENTS & SECURITY RISKS
- Political instability in key transit regions
- Trade disputes and sanctions
- Border closures or restrictions
- Conflicts affecting transportation routes
- Security threats to supply chains (piracy, terrorism, theft)
- Diplomatic relations changes affecting trade
- Infrastructure disruptions due to political decisions


3. MARKET TRENDS & DEMAND SHIFTS
- Seasonal demand patterns and forecasts
- E-commerce growth and its logistics implications
- Industry-specific demand changes (automotive, retail, pharma, etc.)
- Consumer behavior shifts affecting supply chains
- Fuel price trends and forecasts
- Technology adoption in logistics (automation, AI, EVs)
- Sustainability trends affecting logistics practices


4. INFRASTRUCTURE & ROUTE DISRUPTIONS
- Port congestion and capacity issues
- Road, rail, or airport closures and construction
- Weather events affecting transportation routes
- Natural disasters impacting logistics networks
- Technology failures in critical infrastructure
- Strikes and labor disputes
- Capacity constraints in key corridors


5. ECONOMIC FACTORS
- Currency fluctuations affecting international shipping
- Inflation rates in key markets
- Fuel and energy price changes
- Insurance cost trends
- Economic sanctions and their logistics impact
</areas>


Company Profile:
{json.dumps(company_profile, indent=2)}


Search Results (Legal & Regulatory Information):
{json.dumps(search_results, indent=2)}


{feedback_section}


Create a detailed compliance report with the following structure (return as valid JSON):


{{
  "summary": {{
    "total_changes": <number>,
    "overall_risk": "critical|high|medium|low",
    "key_takeaways": ["takeaway 1", "takeaway 2", ...]
  }},
  "legal_changes": [
    {{
      "title": "Change title",
      "description": "Detailed description",
      "effective_date": "YYYY-MM-DD or null",
      "affected_countries": ["DE", "FR", ...],
      "risk_level": "critical|high|medium|low",
      "source_url": "https://..."
    }}
  ],
  "route_impacts": [
    {{
      "route_name": "Route name from company profile",
      "impact_description": "How this route is affected",
      "risk_level": "critical|high|medium|low",
      "recommended_actions": ["action 1", "action 2"]
    }}
  ],
  "recommended_actions": [
    {{
      "priority": "critical|high|medium|low",
      "action": "Specific action to take",
      "deadline": "YYYY-MM-DD or null"
    }}
  ]
}}


Guidelines:
1. Be specific and actionable
2. Cite sources using the URLs from search results
3. Focus on changes that directly impact this company's operations
4. Prioritize by risk level
5. Provide realistic deadlines
6. Ensure all dates are in YYYY-MM-DD format or null
7. Make sure all JSON is properly formatted


Return ONLY valid JSON, no other text."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.content[0].text.strip()

        # Try to extract JSON from response
        try:
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()

            report = json.loads(content)
            return report

        except json.JSONDecodeError as e:
            print(f"   Warning: JSON parse error: {e}")
            print(f"   Content: {content[:200]}...")

            # Return a minimal valid report
            return {
                "summary": {
                    "total_changes": 0,
                    "overall_risk": "medium",
                    "key_takeaways": ["Report generation in progress"]
                },
                "legal_changes": [],
                "route_impacts": [],
                "recommended_actions": []
            }
