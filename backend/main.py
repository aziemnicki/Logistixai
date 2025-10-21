"""
Main FastAPI Application Entry Point.
Logistics Compliance App - Simplified Single-User Backend.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from config import settings
from routes import router
from vector_db import init_vector_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    Initializes resources on startup and cleans up on shutdown.
    """
    # Startup
    print(f"\n{'='*60}")
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"{'='*60}\n")

    # Initialize data directories
    print("📁 Initializing data directories...")
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    os.makedirs(settings.REPORTS_DIR, exist_ok=True)
    os.makedirs(settings.CHAT_HISTORY_DIR, exist_ok=True)
    os.makedirs(settings.CHROMA_DB_PATH, exist_ok=True)

    # Initialize ChromaDB
    print("🗄️  Initializing ChromaDB...")
    try:
        vector_db = init_vector_db()
        report_count = vector_db.count_reports()
        print(f"   ✓ ChromaDB initialized ({report_count} reports in database)")
    except Exception as e:
        print(f"   ⚠️  ChromaDB initialization warning: {e}")

    # Check for company profile
    if os.path.exists(settings.COMPANY_PROFILE_PATH):
        print(f"✓ Company profile found at: {settings.COMPANY_PROFILE_PATH}")
    else:
        print(f"⚠️  No company profile found. Create one at: {settings.COMPANY_PROFILE_PATH}")
        print("   See example_company.json for reference")

    # Configuration summary
    print("\n📋 Configuration:")
    print(f"   • Model: {settings.CLAUDE_MODEL}")
    print(f"   • Data directory: {settings.DATA_DIR}")
    print(f"   • ChromaDB path: {settings.CHROMA_DB_PATH}")
    print(f"   • Max validation iterations: {settings.MAX_VALIDATION_ITERATIONS}")

    if settings.MCP_SERVER_URL:
        print(f"   • MCP Server: {settings.MCP_SERVER_URL}")
    else:
        print("   ⚠️  MCP Server not configured (using mock data)")

    print("\n{'='*60}")
    print("✅ Application started successfully")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("{'='*60}\n")

    yield

    # Shutdown
    print("\n🛑 Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered logistics compliance monitoring application",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# ============================================================================
# MIDDLEWARE
# ============================================================================

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions."""
    print(f"❌ Unhandled exception: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


# ============================================================================
# ROUTES
# ============================================================================

# Include all API routes
app.include_router(router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "profile": "/api/profile",
            "reports": "/api/reports",
            "generate_report": "/api/reports/generate",
            "search_reports": "/api/reports/search?q=query",
            "chat": "/api/chat/{report_id}/message",
            "websocket": "/api/chat/{report_id}/ws",
            "health": "/api/health",
            "stats": "/api/stats"
        }
    }


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

# if __name__ == "__main__":
#     import uvicorn

#     # Run with uvicorn
#     uvicorn.run(
#         "main:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=settings.DEBUG,
#         log_level="info"
#     )
