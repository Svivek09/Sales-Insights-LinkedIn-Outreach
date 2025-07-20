#!/bin/bash

echo "🚀 Setting up Transcript Insight..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Node.js and Python are installed"

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
pip3 install -r requirements.txt
cd ..

# Create .env file if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating .env file..."
    cp backend/env.example backend/.env
    echo "⚠️  Please edit backend/.env with your actual API keys"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your Supabase and OpenAI API keys"
echo "2. Set up your Supabase database using database/schema.sql"
echo "3. Start the backend: cd backend && uvicorn main:app --reload"
echo "4. Start the frontend: npm run dev"
echo ""
echo "📚 See README.md for detailed instructions" 