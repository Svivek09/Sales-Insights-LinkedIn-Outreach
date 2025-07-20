#!/bin/bash

echo "🚀 Starting Transcript Insight Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Creating from template..."
    cp env.example .env
    echo "📝 Please edit .env with your API keys before using the application."
fi

# Start the server
echo "✅ Starting FastAPI server on http://localhost:8000"
echo "📚 API documentation will be available at http://localhost:8000/docs"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

uvicorn main:app --reload --host 127.0.0.1 --port 8000 