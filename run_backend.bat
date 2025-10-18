@echo off
REM Simple script to run the Logistics Compliance Backend on Windows

echo ============================================================
echo Logistics Compliance Backend - Starting...
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "backend\venv\" (
    echo Creating virtual environment...
    cd backend
    python -m venv venv
    cd ..
)

REM Activate virtual environment
echo Activating virtual environment...
call backend\venv\Scripts\activate

REM Check if .env exists
if not exist "backend\.env" (
    echo.
    echo WARNING: .env file not found!
    echo Please copy backend\.env.example to backend\.env
    echo and add your ANTHROPIC_API_KEY
    echo.
    pause
    exit /b 1
)

REM Check if requirements are installed
cd backend
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Run the backend
echo.
echo ============================================================
echo Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python main.py

pause
