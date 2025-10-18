"""
Simplified Data Models for Single-User Logistics Compliance App

These models are streamlined for local development without complex infrastructure.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from enum import Enum


# ============================================================================
# COMPANY PROFILE (Stored in JSON file)
# ============================================================================

class VehicleType(str, Enum):
    """Types of vehicles."""
    TRUCK = "truck"
    VAN = "van"
    SEMI_TRAILER = "semi_trailer"
    REFRIGERATED = "refrigerated"


class CargoCategory(str, Enum):
    """Cargo categories."""
    STANDARD = "standard"
    HAZARDOUS = "hazardous"
    PERISHABLE = "perishable"


class RoutePoint(BaseModel):
    """Simple route point."""
    country_code: str = Field(..., min_length=2, max_length=2)
    city: Optional[str] = None


class TransportRoute(BaseModel):
    """A transport route."""
    name: str
    origin: RoutePoint
    destination: RoutePoint
    transit_countries: List[str] = Field(default_factory=list)


class FleetVehicle(BaseModel):
    """Fleet vehicle info."""
    vehicle_type: VehicleType
    quantity: int = Field(..., gt=0)


class CompanyProfile(BaseModel):
    """Company profile stored in company_profile.json."""
    company_name: str
    contact: Dict[str, str]  # email, phone
    fleet: List[FleetVehicle]
    routes: List[TransportRoute]
    cargo_categories: List[CargoCategory]
    monitoring_preferences: Dict[str, Any] = Field(default_factory=dict)


# ============================================================================
# REPORT MODELS (Stored in SQLite)
# ============================================================================

class ReportStatus(str, Enum):
    """Report status."""
    GENERATING = "generating"
    VALIDATING = "validating"
    APPROVED = "approved"
    REJECTED = "rejected"
    FAILED = "failed"


class RiskLevel(str, Enum):
    """Risk levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ReportSummary(BaseModel):
    """Report executive summary."""
    total_changes: int = Field(0, ge=0)
    overall_risk: RiskLevel
    key_takeaways: List[str]


class LegalChange(BaseModel):
    """A detected legal change."""
    title: str
    description: str
    effective_date: Optional[str] = None
    affected_countries: List[str]
    risk_level: RiskLevel
    source_url: str


class RouteImpact(BaseModel):
    """Impact on a specific route."""
    route_name: str
    impact_description: str
    risk_level: RiskLevel
    recommended_actions: List[str]


class RecommendedAction(BaseModel):
    """Action recommendation."""
    priority: RiskLevel
    action: str
    deadline: Optional[str] = None


class ReportContent(BaseModel):
    """Structured report content."""
    summary: ReportSummary
    legal_changes: List[LegalChange]
    route_impacts: List[RouteImpact]
    recommended_actions: List[RecommendedAction]


class Report(BaseModel):
    """Complete report (stored in SQLite as JSON)."""
    id: str
    company_name: str
    status: ReportStatus
    content: Optional[ReportContent] = None
    generated_at: datetime
    validation_history: List[Dict[str, Any]] = Field(default_factory=list)
    iteration_count: int = Field(0, ge=0, le=3)


# ============================================================================
# AGENT MODELS (Internal use)
# ============================================================================

class SearchResult(BaseModel):
    """Single search result from MCP."""
    url: str
    title: str
    snippet: str
    published_date: Optional[str] = None


class AgentInput(BaseModel):
    """Generic agent input."""
    company_profile: CompanyProfile
    search_results: Optional[List[SearchResult]] = None
    previous_feedback: Optional[str] = None


class AgentOutput(BaseModel):
    """Generic agent output."""
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None


# ============================================================================
# CHAT MODELS
# ============================================================================

class ChatMessage(BaseModel):
    """Single chat message."""
    id: str
    report_id: str
    role: str  # "user" or "assistant"
    content: str
    sources: Optional[List[str]] = None
    created_at: datetime


class ChatHistory(BaseModel):
    """Chat history for a report."""
    report_id: str
    messages: List[ChatMessage]


# ============================================================================
# API REQUEST/RESPONSE MODELS
# ============================================================================

class GenerateReportRequest(BaseModel):
    """Request to generate report."""
    force_refresh: bool = False


class GenerateReportResponse(BaseModel):
    """Response for report generation."""
    report_id: str
    status: str
    message: str


class ReportListResponse(BaseModel):
    """List of reports."""
    reports: List[Report]
    total: int


class ChatMessageRequest(BaseModel):
    """Send chat message."""
    message: str = Field(..., min_length=1, max_length=2000)


class ChatMessageResponse(BaseModel):
    """Chat message response."""
    message_id: str
    content: str
    sources: Optional[List[str]] = None
    created_at: datetime


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Health check."""
    status: str = "ok"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
