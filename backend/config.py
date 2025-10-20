"""
Configuration management for the Logistics Compliance App.
Loads settings from environment variables and .env file using python-dotenv.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

# Determine the correct path to .env file
# Try multiple locations to ensure we find it
current_dir = Path(__file__).parent
backend_env = current_dir / '.env'
root_env = current_dir.parent / '.env'

# Load .env file from the most appropriate location
if backend_env.exists():
    load_dotenv(dotenv_path=backend_env, override=True)
    print(f"✓ Loaded configuration from: {backend_env}")
elif root_env.exists():
    load_dotenv(dotenv_path=root_env, override=True)
    print(f"✓ Loaded configuration from: {root_env}")
else:
    print(f"⚠️  No .env file found. Using environment variables and defaults.")
    print(f"   Searched in: {backend_env} and {root_env}")


class Settings(BaseSettings):
    """Application settings loaded from .env file and environment variables."""

    # ========================================================================
    # REQUIRED CONFIGURATION
    # ========================================================================

    # Anthropic API Key (Optional - can be provided by user at runtime)
    # Get your API key from: https://console.anthropic.com/
    ANTHROPIC_API_KEY: Optional[str] = None

    # ========================================================================
    # OPTIONAL CONFIGURATION
    # ========================================================================

    # MCP Server Configuration (Optional - uses mock data if not configured)
    # For Gate22 ACI.dev MCP Gateway
    MCP_GATEWAY_URL: Optional[str] = None
    MCP_API_KEY: Optional[str] = None

    # Legacy MCP configuration (deprecated but supported)
    MCP_SERVER_URL: Optional[str] = None

    # Application Settings
    APP_NAME: str = "Logistics Compliance App"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Optional Authentication (leave empty for no auth)
    APP_PASSWORD: Optional[str] = None
    SECRET_KEY: Optional[str] = None

    # Data Storage Paths (relative to backend directory)
    DATA_DIR: str = "./data"
    CHROMA_DB_PATH: str = "./data/chroma_data"
    COMPANY_PROFILE_PATH: str = "./data/company_profile.json"
    REPORTS_DIR: str = "./data/reports"
    CHAT_HISTORY_DIR: str = "./data/chat_history"

    # AI Agent Configuration
    CLAUDE_MODEL: str = "claude-haiku-4-5"
    MAX_VALIDATION_ITERATIONS: int = 3
    USE_MCP_AGENTS: bool = True  # Enable MCP-powered agents when available

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env

    def __init__(self, **kwargs):
        """Initialize settings and validate required fields."""
        super().__init__(**kwargs)

        # Normalize empty strings to None
        if not self.ANTHROPIC_API_KEY or self.ANTHROPIC_API_KEY.strip() == "":
            self.ANTHROPIC_API_KEY = None
            print("⚠️  Warning: No ANTHROPIC_API_KEY in .env. Users must provide their own API key.")
        elif self.ANTHROPIC_API_KEY == "your_anthropic_api_key_here":
            self.ANTHROPIC_API_KEY = None
            print("⚠️  Warning: ANTHROPIC_API_KEY placeholder detected. Users will need to provide their own API key.")


# Global settings instance
try:
    settings = Settings()
    print(f"✓ Settings initialized successfully")
    print(f"  • Model: {settings.CLAUDE_MODEL}")
    print(f"  • Data directory: {settings.DATA_DIR}")
    print(f"  • Debug mode: {settings.DEBUG}")
    if settings.MCP_SERVER_URL:
        print(f"  • MCP Server: {settings.MCP_SERVER_URL}")
except ValueError as e:
    print(f"\n❌ Configuration Error:\n{e}\n")
    raise
except Exception as e:
    print(f"\n❌ Unexpected configuration error: {e}\n")
    raise
