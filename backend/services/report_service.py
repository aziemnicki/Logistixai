"""
Report Service - Orchestrates the multi-agent report generation pipeline.
Manages the flow: Search → Generate → Validate (up to 3 iterations).
"""

from agents import SearchAgent, ReportGeneratorAgent, ValidatorAgent
from vector_db import vector_db
from config import settings
from mcp_config import is_mcp_configured
from services.pdf_service import pdf_service

# Try to import MCP-enabled agent
try:
    from agents.search_agent_mcp import MCPSearchAgent
    MCP_AGENT_AVAILABLE = True
except ImportError:
    MCP_AGENT_AVAILABLE = False
from typing import Dict, Any, Optional
import json
import os
from datetime import datetime
import uuid


class ReportService:
    """Service for orchestrating report generation with multi-agent workflow."""

    def __init__(self):
        """Initialize report service."""
        self.vector_db = vector_db

        # Ensure data directories exist
        os.makedirs(settings.REPORTS_DIR, exist_ok=True)
        os.makedirs(settings.CHAT_HISTORY_DIR, exist_ok=True)

    async def generate_report(
        self,
        company_profile: Dict[str, Any],
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a complete validated compliance report.

        Args:
            company_profile: Company profile data
            api_key: Optional Anthropic API key

        Returns:
            Dictionary with report data and metadata
        """
        print(f"\n{'='*60}")
        print(f"🚀 Starting Report Generation Pipeline")
        print(f"   Company: {company_profile.get('company_name', 'Unknown')}")
        print(f"{'='*60}\n")

        report_id = str(uuid.uuid4())
        iteration_count = 0
        validation_history = []

        try:
            # Create agents with provided API key
            # Choose search agent based on MCP availability and configuration
            if settings.USE_MCP_AGENTS and MCP_AGENT_AVAILABLE and is_mcp_configured():
                print("✓ Using MCP-enabled Search Agent (autonomous mode)")
                search_agent = MCPSearchAgent(api_key=api_key)
            else:
                print("✓ Using standard Search Agent (fallback mode)")
                search_agent = SearchAgent(api_key=api_key)

            report_agent = ReportGeneratorAgent(api_key=api_key)
            validator_agent = ValidatorAgent(api_key=api_key)

            # Step 1: Search Agent - Gather data
            print(f"[1/3] Search Phase")
            search_result = await search_agent.execute(company_profile)

            if not search_result["success"]:
                raise Exception(f"Search failed: {search_result.get('error')}")

            search_results = search_result["search_results"]

            # Store search results in ChromaDB for RAG
            self.vector_db.add_search_results(report_id, search_results)

            # Step 2: Report Generation with Validation Loop
            print(f"\n[2/3] Report Generation Phase")

            report_content = None
            previous_feedback = None
            max_iterations = settings.MAX_VALIDATION_ITERATIONS

            while iteration_count < max_iterations:
                iteration_count += 1
                print(f"\n   Iteration {iteration_count}/{max_iterations}")

                # Generate report
                report_result = await report_agent.execute(
                    company_profile=company_profile,
                    search_results=search_results,
                    previous_feedback=previous_feedback
                )

                if not report_result["success"]:
                    raise Exception(f"Report generation failed: {report_result.get('error')}")

                report_content = report_result["report"]

                # Step 3: Validate report
                print(f"\n[3/3] Validation Phase (Iteration {iteration_count})")

                validation_result = await validator_agent.execute(
                    report=report_content,
                    company_profile=company_profile,
                    search_results=search_results
                )

                validation_entry = {
                    "iteration": iteration_count,
                    "is_approved": validation_result.get("is_approved", False),
                    "quality_score": validation_result.get("quality_score", 0),
                    "feedback": validation_result.get("feedback", ""),
                    "issues": validation_result.get("issues", []),
                    "validated_at": datetime.utcnow().isoformat()
                }
                validation_history.append(validation_entry)

                # Check if approved
                if validation_result.get("is_approved", False):
                    print(f"\n✅ Report approved after {iteration_count} iteration(s)")
                    break

                # Not approved, prepare for next iteration
                previous_feedback = validation_result.get("feedback", "")
                print(f"   ⚠️  Report needs improvement. Regenerating...")

                # If max iterations reached, accept anyway
                if iteration_count >= max_iterations:
                    print(f"\n⚠️  Max iterations reached. Accepting current version.")
                    break

            # Build final report object
            final_report = {
                "id": report_id,
                "company_name": company_profile.get("company_name", "Unknown"),
                "status": "approved",
                "content": report_content,
                "generated_at": datetime.utcnow().isoformat(),
                "validation_history": validation_history,
                "iteration_count": iteration_count,
                "search_metadata": {
                    "total_sources": len(search_results),
                    "queries_used": search_result.get("queries_used", [])
                }
            }

            # Save report to JSON file
            report_path = os.path.join(settings.REPORTS_DIR, f"{report_id}.json")
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(final_report, f, indent=2, ensure_ascii=False)

            print(f"\n💾 Report saved to: {report_path}")

            # Store report in ChromaDB for semantic search and RAG
            report_text = json.dumps(report_content, ensure_ascii=False)
            self.vector_db.add_report(
                report_id=report_id,
                report_content=report_text,
                metadata={
                    "report_id": report_id,
                    "company_name": company_profile.get("company_name", "Unknown"),
                    "generated_at": final_report["generated_at"],
                    "status": final_report["status"],
                    "overall_risk": report_content.get("summary", {}).get("overall_risk", "medium")
                }
            )

            print(f"📊 Report stored in ChromaDB for semantic search")

            # Generate PDF report
            try:
                print(f"📄 Generating PDF report...")

                # Create PDF directory if it doesn't exist
                pdf_dir = os.path.join(settings.REPORTS_DIR, "pdfs")
                os.makedirs(pdf_dir, exist_ok=True)

                pdf_path = os.path.join(pdf_dir, f"{report_id}.pdf")

                # Generate PDF with sources
                pdf_service.generate_pdf(
                    report_data=final_report,
                    output_path=pdf_path,
                    sources=search_results
                )

                print(f"   ✓ PDF generated: {pdf_path}")

                # Store PDF metadata in vector database
                pdf_metadata = {
                    "company_name": company_profile.get("company_name", "Unknown"),
                    "generated_at": final_report["generated_at"],
                    "status": final_report["status"],
                    "file_size_kb": os.path.getsize(pdf_path) / 1024,
                    "format": "pdf"
                }

                # We don't store the full base64 in ChromaDB for large files
                # Instead, we store the path and metadata
                pdf_base64 = ""  # Empty for now, file path is enough

                self.vector_db.add_pdf(
                    report_id=report_id,
                    pdf_base64=pdf_base64,
                    pdf_path=pdf_path,
                    metadata=pdf_metadata
                )

                print(f"   ✓ PDF metadata stored in ChromaDB")

                # Add PDF path to final report
                final_report["pdf_path"] = pdf_path
                final_report["has_pdf"] = True

            except Exception as pdf_error:
                print(f"   ⚠️  PDF generation failed: {pdf_error}")
                final_report["pdf_path"] = None
                final_report["has_pdf"] = False

            print(f"\n{'='*60}")
            print(f"✅ Report Generation Complete!")
            print(f"   Report ID: {report_id}")
            print(f"   Iterations: {iteration_count}")
            if final_report.get("has_pdf"):
                print(f"   PDF Available: Yes")
            print(f"{'='*60}\n")

            return {
                "success": True,
                "report": final_report
            }

        except Exception as e:
            print(f"\n{'='*60}")
            print(f"❌ Report Generation Failed")
            print(f"   Error: {str(e)}")
            print(f"{'='*60}\n")

            # Save failed report
            failed_report = {
                "id": report_id,
                "company_name": company_profile.get("company_name", "Unknown"),
                "status": "failed",
                "error": str(e),
                "generated_at": datetime.utcnow().isoformat(),
                "iteration_count": iteration_count,
                "validation_history": validation_history
            }

            report_path = os.path.join(settings.REPORTS_DIR, f"{report_id}.json")
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(failed_report, f, indent=2, ensure_ascii=False)

            return {
                "success": False,
                "error": str(e),
                "report": failed_report
            }

    def get_all_reports(self) -> list:
        """Get all reports from JSON files."""
        reports = []

        if not os.path.exists(settings.REPORTS_DIR):
            return reports

        for filename in os.listdir(settings.REPORTS_DIR):
            if filename.endswith(".json"):
                try:
                    report_path = os.path.join(settings.REPORTS_DIR, filename)
                    with open(report_path, "r", encoding="utf-8") as f:
                        report = json.load(f)
                        reports.append(report)
                except Exception as e:
                    print(f"Warning: Could not load report {filename}: {e}")

        # Sort by generated_at descending
        reports.sort(key=lambda x: x.get("generated_at", ""), reverse=True)

        return reports

    def get_report_by_id(self, report_id: str) -> Dict[str, Any]:
        """Get a specific report by ID."""
        report_path = os.path.join(settings.REPORTS_DIR, f"{report_id}.json")

        if not os.path.exists(report_path):
            return None

        try:
            with open(report_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading report {report_id}: {e}")
            return None

    def search_reports(self, query: str, limit: int = 10) -> list:
        """
        Search reports using ChromaDB semantic search.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching reports with relevance scores
        """
        results = self.vector_db.search_reports(query, n_results=limit)

        matched_reports = []
        if results.get("ids") and results["ids"][0]:
            for report_id, distance in zip(results["ids"][0], results["distances"][0]):
                report = self.get_report_by_id(report_id)
                if report:
                    report["relevance_score"] = 1 - distance  # Convert distance to similarity
                    matched_reports.append(report)

        return matched_reports

    def delete_report(self, report_id: str) -> bool:
        """Delete a report and all associated data."""
        try:
            # Delete JSON file
            report_path = os.path.join(settings.REPORTS_DIR, f"{report_id}.json")
            if os.path.exists(report_path):
                os.remove(report_path)

            # Delete from ChromaDB
            self.vector_db.delete_report(report_id)

            # Delete chat history
            chat_path = os.path.join(settings.CHAT_HISTORY_DIR, f"{report_id}_chat.json")
            if os.path.exists(chat_path):
                os.remove(chat_path)

            return True
        except Exception as e:
            print(f"Error deleting report {report_id}: {e}")
            return False


# Global service instance
report_service = ReportService()
