#!/bin/bash
# Simple script to run the Logistics Compliance Backend on Linux/Mac

echo "============================================================"
echo "Logistics Compliance Backend - Starting..."
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "Creating virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# Activate virtual environment
echo "Activating virtual environment..."
source backend/venv/bin/activate

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo "Please copy backend/.env.example to backend/.env"
    echo "and add your ANTHROPIC_API_KEY"
    echo ""
    exit 1
fi

# Check if requirements are installed
cd backend
if ! pip show fastapi &> /dev/null; then
    echo ""
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the backend
echo ""
echo "============================================================"
echo "Starting FastAPI server on http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo "============================================================"
echo ""

python main.py
