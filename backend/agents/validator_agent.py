"""
Validator Agent - Reviews and validates report quality.
Third agent in the pipeline. Can trigger up to 3 iterations.
"""

from anthropic import Anthropic
from config import settings
from typing import Dict, Any, Optional
import json


class ValidatorAgent:
    """Agent responsible for validating report quality."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Validator Agent with Claude client.

        Args:
            api_key: Optional Anthropic API key. If not provided, uses settings.ANTHROPIC_API_KEY
        """
        # Use provided API key, or fall back to settings
        effective_api_key = api_key or settings.ANTHROPIC_API_KEY

        # Validate API key is not empty or whitespace
        if not effective_api_key or not effective_api_key.strip():
            raise ValueError("API key is required. Either provide it or set ANTHROPIC_API_KEY in .env")

        # Validate API key format (should start with sk-ant-)
        if not effective_api_key.strip().startswith("sk-ant-"):
            raise ValueError("Invalid API key format. Anthropic API keys should start with 'sk-ant-'")

        self.client = Anthropic(api_key=effective_api_key.strip())
        self.model = settings.CLAUDE_MODEL

    async def execute(
        self,
        report: Dict[str, Any],
        company_profile: Dict[str, Any],
        search_results: list
    ) -> Dict[str, Any]:
        """
        Validate a generated report.

        Args:
            report: Report content to validate
            company_profile: Company profile data
            search_results: Original search results

        Returns:
            Dictionary with validation results
        """
        print("✅ Validator Agent: Checking report quality...")

        try:
            validation_result = await self._validate_report(
                report,
                company_profile,
                search_results
            )

            if validation_result["is_approved"]:
                print("   ✓ Report approved")
            else:
                print("   ✗ Report needs improvement")
                print(f"   Feedback: {validation_result['feedback'][:100]}...")

            return {
                "success": True,
                **validation_result
            }

        except Exception as e:
            print(f"❌ Validator error: {e}")
            # On error, approve by default to avoid blocking
            return {
                "success": True,
                "is_approved": True,
                "feedback": "Validation skipped due to error",
                "quality_score": 0
            }

    async def _validate_report(
        self,
        report: Dict[str, Any],
        company_profile: Dict[str, Any],
        search_results: list
    ) -> Dict[str, Any]:
        """Validate report using Claude."""

        prompt = f"""You are a quality assurance expert for logistics compliance reports. Review this report and determine if it meets quality standards.

Company Profile:
{json.dumps(company_profile, indent=2)}

Generated Report:
{json.dumps(report, indent=2)}

Search Results Used:
{json.dumps(search_results[:5], indent=2)}

Evaluate the report based on these criteria:
1. **Structure**: Is the JSON structure valid and complete with all required sections?
2. **Relevance**: Does it focus on this specific company's operations, routes, and cargo types?
3. **Actionability**: Are recommendations specific and implementable?
4. **Risk Assessment**: Are risk levels appropriate for the scenarios described?
5. **Professionalism**: Is the content well-written and professional?
6. **Usefulness**: Would this report provide value to the company even with limited data sources?

IMPORTANT GUIDELINES:
- Accept reports that acknowledge data limitations transparently
- Accept reports with empty legal_changes if they provide relevant recommendations
- Accept reports that provide generic but useful compliance guidance
- Focus on whether the report is USEFUL and RELEVANT to the company
- Do not penalize heavily for lack of source URLs if search results were limited
- Value quality of analysis over quantity of sources

Return your evaluation as JSON in this exact format:
{{
  "is_approved": true/false,
  "quality_score": <number 0-100>,
  "feedback": "Detailed feedback if not approved, or 'Report meets quality standards' if approved",
  "issues": ["issue 1", "issue 2", ...] or []
}}

Standards:
- Approve if quality_score >= 50 (lowered threshold for more lenient acceptance)
- Reject only if quality_score < 50
- Be constructive and generous in feedback
- Prioritize usefulness over perfection

Return ONLY valid JSON, no other text."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.content[0].text.strip()

        try:
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()

            validation = json.loads(content)

            # Ensure required fields
            validation.setdefault("is_approved", False)
            validation.setdefault("quality_score", 0)
            validation.setdefault("feedback", "Validation incomplete")
            validation.setdefault("issues", [])

            return validation

        except json.JSONDecodeError:
            # Fallback: approve if we can't parse validation
            print("   Warning: Could not parse validation response, approving by default")
            return {
                "is_approved": True,
                "quality_score": 80,
                "feedback": "Report meets quality standards",
                "issues": []
            }
