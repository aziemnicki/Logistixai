"""
API Routes for Logistics Compliance App.
Defines all REST and WebSocket endpoints.
"""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Query, Header
from fastapi.responses import FileResponse
from typing import Optional
import json
import os
from datetime import datetime

from config import settings
from services import report_service, chat_service
from vector_db import vector_db
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simplified_models import (
    CompanyProfile,
    GenerateReportRequest,
    GenerateReportResponse,
    ReportListResponse,
    ChatMessageRequest,
    ChatMessageResponse,
    ErrorResponse,
    HealthCheckResponse
)

# Create router
router = APIRouter()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_api_key(x_api_key: Optional[str] = Header(None)) -> Optional[str]:
    """Extract API key from request header or fall back to environment variable."""
    return x_api_key or settings.ANTHROPIC_API_KEY


# ============================================================================
# COMPANY PROFILE ENDPOINTS
# ============================================================================

@router.get("/api/profile", response_model=CompanyProfile)
async def get_company_profile():
    """Get company profile from JSON file."""
    profile_path = settings.COMPANY_PROFILE_PATH

    if not os.path.exists(profile_path):
        raise HTTPException(
            status_code=404,
            detail="Company profile not found. Please create company_profile.json"
        )

    try:
        with open(profile_path, "r", encoding="utf-8") as f:
            profile_data = json.load(f)
            return CompanyProfile(**profile_data)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading company profile: {str(e)}"
        )


@router.put("/api/profile", response_model=CompanyProfile)
async def update_company_profile(profile: CompanyProfile):
    """Update company profile."""
    profile_path = settings.COMPANY_PROFILE_PATH

    # Ensure data directory exists
    os.makedirs(os.path.dirname(profile_path), exist_ok=True)

    try:
        with open(profile_path, "w", encoding="utf-8") as f:
            json.dump(profile.model_dump(), f, indent=2, ensure_ascii=False)
        return profile
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving company profile: {str(e)}"
        )


# ============================================================================
# REPORT ENDPOINTS
# ============================================================================

@router.post("/api/reports/generate", response_model=GenerateReportResponse)
async def generate_report(request: GenerateReportRequest, api_key: Optional[str] = Header(None, alias="X-API-Key")):
    """
    Generate a new compliance report.
    This triggers the multi-agent pipeline: Search → Generate → Validate.
    """
    # Get effective API key (from header or environment)
    effective_api_key = api_key or settings.ANTHROPIC_API_KEY

    # Validate API key
    if not effective_api_key or not effective_api_key.strip():
        raise HTTPException(
            status_code=400,
            detail="API key is required. Please provide your Anthropic API key."
        )

    if not effective_api_key.strip().startswith("sk-ant-"):
        raise HTTPException(
            status_code=400,
            detail="Invalid API key format. Anthropic API keys should start with 'sk-ant-'"
        )

    # Load company profile
    profile_path = settings.COMPANY_PROFILE_PATH

    if not os.path.exists(profile_path):
        raise HTTPException(
            status_code=400,
            detail="Company profile not found. Please create company profile first."
        )

    try:
        with open(profile_path, "r", encoding="utf-8") as f:
            company_profile = json.load(f)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading company profile: {str(e)}"
        )

    # Generate report
    try:
        result = await report_service.generate_report(company_profile, api_key=effective_api_key)

        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Report generation failed")
            )

        report = result["report"]

        return GenerateReportResponse(
            report_id=report["id"],
            status=report["status"],
            message=f"Report generated successfully after {report['iteration_count']} iteration(s)"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating report: {str(e)}"
        )


@router.get("/api/reports", response_model=ReportListResponse)
async def list_reports(
    limit: Optional[int] = Query(50, ge=1, le=100),
    offset: Optional[int] = Query(0, ge=0)
):
    """Get list of all reports."""
    try:
        all_reports = report_service.get_all_reports()

        # Apply pagination
        paginated = all_reports[offset:offset + limit]

        return ReportListResponse(
            reports=paginated,
            total=len(all_reports)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving reports: {str(e)}"
        )


@router.get("/api/reports/search")
async def search_reports(
    q: str = Query(..., min_length=1),
    limit: Optional[int] = Query(10, ge=1, le=50)
):
    """
    Search reports using semantic search (ChromaDB).

    Args:
        q: Search query
        limit: Maximum number of results
    """
    try:
        results = report_service.search_reports(q, limit=limit)

        return {
            "query": q,
            "results": results,
            "total": len(results)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching reports: {str(e)}"
        )


@router.get("/api/reports/{report_id}")
async def get_report(report_id: str):
    """Get a specific report by ID."""
    try:
        report = report_service.get_report_by_id(report_id)

        if not report:
            raise HTTPException(
                status_code=404,
                detail=f"Report {report_id} not found"
            )

        return report

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving report: {str(e)}"
        )


@router.delete("/api/reports/{report_id}")
async def delete_report(report_id: str):
    """Delete a report and all associated data."""
    try:
        success = report_service.delete_report(report_id)

        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Report {report_id} not found or could not be deleted"
            )

        return {"message": f"Report {report_id} deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting report: {str(e)}"
        )


# ============================================================================
# PDF ENDPOINTS
# ============================================================================

@router.get("/api/reports/{report_id}/pdf")
async def download_report_pdf(report_id: str):
    """
    Download PDF version of a report.

    Args:
        report_id: Report identifier

    Returns:
        PDF file
    """
    try:
        # Get PDF metadata from vector database
        pdf_metadata = vector_db.get_pdf_metadata(report_id)

        if not pdf_metadata:
            raise HTTPException(
                status_code=404,
                detail=f"PDF not found for report {report_id}"
            )

        pdf_path = pdf_metadata.get("pdf_path")

        if not pdf_path or not os.path.exists(pdf_path):
            raise HTTPException(
                status_code=404,
                detail=f"PDF file not found at expected location"
            )

        # Return PDF file
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=f"compliance_report_{report_id}.pdf"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving PDF: {str(e)}"
        )


@router.get("/api/reports/pdfs/search")
async def search_pdfs(
    q: str = Query(..., min_length=1),
    limit: Optional[int] = Query(10, ge=1, le=50)
):
    """
    Search for PDF reports using semantic search.

    Args:
        q: Search query
        limit: Maximum results

    Returns:
        List of PDF metadata
    """
    try:
        results = vector_db.search_pdfs(q, n_results=limit)

        return {
            "query": q,
            "results": results,
            "total": len(results)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching PDFs: {str(e)}"
        )


@router.get("/api/reports/{report_id}/pdf/info")
async def get_pdf_info(report_id: str):
    """
    Get PDF metadata for a report.

    Args:
        report_id: Report identifier

    Returns:
        PDF metadata
    """
    try:
        pdf_metadata = vector_db.get_pdf_metadata(report_id)

        if not pdf_metadata:
            raise HTTPException(
                status_code=404,
                detail=f"PDF metadata not found for report {report_id}"
            )

        return {
            "report_id": report_id,
            "metadata": pdf_metadata,
            "available": os.path.exists(pdf_metadata.get("pdf_path", ""))
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving PDF info: {str(e)}"
        )


# ============================================================================
# CHAT ENDPOINTS
# ============================================================================

@router.get("/api/chat/{report_id}/history")
async def get_chat_history(report_id: str):
    """Get chat history for a report."""
    try:
        # Verify report exists
        report = report_service.get_report_by_id(report_id)
        if not report:
            raise HTTPException(
                status_code=404,
                detail=f"Report {report_id} not found"
            )

        history = chat_service.get_chat_history(report_id)
        return history

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving chat history: {str(e)}"
        )


@router.post("/api/chat/{report_id}/message", response_model=ChatMessageResponse)
async def send_chat_message(report_id: str, request: ChatMessageRequest, api_key: Optional[str] = Header(None, alias="X-API-Key")):
    """Send a chat message and get AI response."""
    # Get effective API key (from header or environment)
    effective_api_key = api_key or settings.ANTHROPIC_API_KEY

    # Validate API key
    if not effective_api_key or not effective_api_key.strip():
        raise HTTPException(
            status_code=400,
            detail="API key is required. Please provide your Anthropic API key."
        )

    if not effective_api_key.strip().startswith("sk-ant-"):
        raise HTTPException(
            status_code=400,
            detail="Invalid API key format. Anthropic API keys should start with 'sk-ant-'"
        )

    try:
        # Verify report exists
        report = report_service.get_report_by_id(report_id)
        if not report:
            raise HTTPException(
                status_code=404,
                detail=f"Report {report_id} not found"
            )

        # Send message
        result = await chat_service.send_message(
            report_id=report_id,
            message=request.message,
            api_key=effective_api_key
        )

        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Failed to process message")
            )

        message = result["message"]

        return ChatMessageResponse(
            message_id=message["id"],
            content=message["content"],
            sources=message.get("sources", []),
            created_at=datetime.fromisoformat(message["created_at"])
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing message: {str(e)}"
        )


@router.get("/api/chat/{report_id}/suggestions")
async def get_suggested_questions(report_id: str, api_key: Optional[str] = Header(None, alias="X-API-Key")):
    """Get suggested follow-up questions."""
    # Get effective API key (from header or environment)
    effective_api_key = api_key or settings.ANTHROPIC_API_KEY

    # Validate API key
    if not effective_api_key or not effective_api_key.strip():
        raise HTTPException(
            status_code=400,
            detail="API key is required. Please provide your Anthropic API key."
        )

    if not effective_api_key.strip().startswith("sk-ant-"):
        raise HTTPException(
            status_code=400,
            detail="Invalid API key format. Anthropic API keys should start with 'sk-ant-'"
        )

    try:
        # Verify report exists
        report = report_service.get_report_by_id(report_id)
        if not report:
            raise HTTPException(
                status_code=404,
                detail=f"Report {report_id} not found"
            )

        suggestions = await chat_service.generate_suggested_questions(report_id, api_key=effective_api_key)

        return {
            "report_id": report_id,
            "suggestions": suggestions
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating suggestions: {str(e)}"
        )


@router.delete("/api/chat/{report_id}/history")
async def clear_chat_history(report_id: str):
    """Clear chat history for a report."""
    try:
        success = chat_service.clear_chat_history(report_id)

        if not success:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to clear chat history for {report_id}"
            )

        return {"message": f"Chat history cleared for {report_id}"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing chat history: {str(e)}"
        )


# ============================================================================
# WEBSOCKET ENDPOINT (Alternative to REST for real-time chat)
# ============================================================================

@router.websocket("/api/chat/{report_id}/ws")
async def websocket_chat(websocket: WebSocket, report_id: str):
    """
    WebSocket endpoint for real-time chat.

    Send JSON: {"message": "your question"}
    Receive JSON: {"type": "message", "content": "...", "sources": [...]}
    """
    await websocket.accept()

    try:
        # Verify report exists
        report = report_service.get_report_by_id(report_id)
        if not report:
            await websocket.send_json({
                "type": "error",
                "error": f"Report {report_id} not found"
            })
            await websocket.close()
            return

        # Send welcome message
        await websocket.send_json({
            "type": "info",
            "message": f"Connected to chat for report {report_id}"
        })

        # Chat loop
        while True:
            # Receive message
            data = await websocket.receive_json()
            message = data.get("message", "").strip()

            if not message:
                await websocket.send_json({
                    "type": "error",
                    "error": "Empty message"
                })
                continue

            # Process message
            result = await chat_service.send_message(
                report_id=report_id,
                message=message
            )

            if result["success"]:
                response_data = result["message"]
                await websocket.send_json({
                    "type": "message",
                    "message_id": response_data["id"],
                    "content": response_data["content"],
                    "sources": response_data.get("sources", []),
                    "created_at": response_data["created_at"]
                })
            else:
                await websocket.send_json({
                    "type": "error",
                    "error": result.get("error", "Unknown error")
                })

    except WebSocketDisconnect:
        print(f"WebSocket disconnected for report {report_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "error": str(e)
            })
        except:
            pass


# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@router.get("/api/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    return HealthCheckResponse(
        status="ok",
        timestamp=datetime.utcnow()
    )


@router.get("/api/stats")
async def get_stats():
    """Get application statistics."""
    try:
        from vector_db import vector_db

        reports = report_service.get_all_reports()

        return {
            "total_reports": len(reports),
            "reports_in_chromadb": vector_db.count_reports(),
            "approved_reports": len([r for r in reports if r.get("status") == "approved"]),
            "failed_reports": len([r for r in reports if r.get("status") == "failed"]),
            "data_directory": settings.DATA_DIR,
            "chromadb_path": settings.CHROMA_DB_PATH
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving stats: {str(e)}"
        )
