@echo off
REM Fox AI Platform - Quick Start Script for Windows

echo 🦊 Starting Fox AI Platform...

REM Check if .env exists
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo ⚠️  Edit .env file to add your API keys!
)

REM Check if Docker is available
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo 🐳 Starting with Docker...
    docker-compose up -d
    echo.
    echo ✅ Fox AI Platform is running!
    echo 🌐 Open http://localhost:8000 in your browser
    echo.
    echo 📝 To view logs: docker-compose logs -f
    echo 🛑 To stop: docker-compose down
) else (
    echo Docker not found. Starting with Python...
    
    REM Create venv if it doesn't exist
    if not exist venv (
        echo Creating virtual environment...
        python -m venv venv
    )
    
    REM Activate venv
    call venv\Scripts\activate.bat
    
    REM Install dependencies
    echo Installing dependencies...
    pip install -r backend\requirements.txt
    
    REM Start server
    echo Starting server...
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
)
