#!/bin/bash

# Fox AI Platform - Quick Start Script

echo "🦊 Starting Fox AI Platform..."

# Check if .env exists, if not create from example
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Edit .env file to add your API keys!"
fi

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "🐳 Starting with Docker..."
    docker-compose up -d
    echo ""
    echo "✅ Fox AI Platform is running!"
    echo "🌐 Open http://localhost:8000 in your browser"
    echo ""
    echo "📝 To view logs: docker-compose logs -f"
    echo "🛑 To stop: docker-compose down"
else
    echo "Docker not found. Starting with Python..."
    
    # Create venv if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate venv
    source venv/bin/activate
    
    # Install dependencies
    echo "Installing dependencies..."
    pip install -r backend/requirements.txt
    
    # Start server
    echo "Starting server..."
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
fi
