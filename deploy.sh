#!/bin/bash

# Deployment script for Transcript Insight & LinkedIn Icebreaker
# This script helps set up the initial deployment to GitHub, Render, and Netlify

set -e  # Exit on any error

echo "🚀 Starting deployment process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -f "backend/main.py" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_status "Checking prerequisites..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install Git first."
    exit 1
fi

# Check if node is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm first."
    exit 1
fi

print_success "Prerequisites check passed"

# Install frontend dependencies
print_status "Installing frontend dependencies..."
npm install
print_success "Frontend dependencies installed"

# Install Radix UI tabs if not already installed
if ! npm list @radix-ui/react-tabs &> /dev/null; then
    print_status "Installing missing Radix UI tabs dependency..."
    npm install @radix-ui/react-tabs
    print_success "Radix UI tabs installed"
fi

# Check if git repository is initialized
if [ ! -d ".git" ]; then
    print_status "Initializing Git repository..."
    git init
    print_success "Git repository initialized"
fi

# Check if .gitignore exists
if [ ! -f ".gitignore" ]; then
    print_error ".gitignore file is missing. Please create it first."
    exit 1
fi

# Add all files to git
print_status "Adding files to Git..."
git add .
print_success "Files added to Git"

# Check if there are changes to commit
if git diff --cached --quiet; then
    print_warning "No changes to commit. Repository is up to date."
else
    print_status "Committing changes..."
    git commit -m "Prepare for deployment: Add deployment configuration and fix dependencies"
    print_success "Changes committed"
fi

# Check if remote origin is set
if ! git remote get-url origin &> /dev/null; then
    print_warning "No remote origin set. You'll need to add your GitHub repository manually."
    echo ""
    echo "To add your GitHub repository, run:"
    echo "git remote add origin https://github.com/yourusername/transcript-insight.git"
    echo "git push -u origin main"
    echo ""
else
    print_status "Remote origin is configured"
    echo "Current remote URL: $(git remote get-url origin)"
fi

# Test build
print_status "Testing frontend build..."
if npm run build; then
    print_success "Frontend build successful"
else
    print_error "Frontend build failed. Please fix the issues before deploying."
    exit 1
fi

# Test backend
print_status "Testing backend..."
cd backend
if python -c "import main; print('Backend imports successful')" 2>/dev/null; then
    print_success "Backend test successful"
else
    print_warning "Backend test failed. Make sure you have the required Python packages installed."
    echo "To install backend dependencies, run:"
    echo "cd backend"
    echo "pip install -r requirements.txt"
fi
cd ..

echo ""
print_success "Deployment preparation completed!"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. 🐙 GitHub Setup:"
echo "   - Create a new repository on GitHub"
echo "   - Add it as remote: git remote add origin https://github.com/yourusername/transcript-insight.git"
echo "   - Push your code: git push -u origin main"
echo ""
echo "2. 🎯 Render Backend Deployment:"
echo "   - Go to https://render.com"
echo "   - Create new Web Service"
echo "   - Connect your GitHub repository"
echo "   - Set Root Directory to 'backend'"
echo "   - Set Runtime to 'Docker'"
echo "   - Add environment variables:"
echo "     * GOOGLE_API_KEY=your_gemini_api_key"
echo "     * SUPABASE_URL=your_supabase_url"
echo "     * SUPABASE_KEY=your_supabase_key"
echo ""
echo "3. 🌐 Netlify Frontend Deployment:"
echo "   - Go to https://netlify.com"
echo "   - Create new site from Git"
echo "   - Connect your GitHub repository"
echo "   - Set Build command: npm run build"
echo "   - Set Publish directory: .next"
echo "   - Add environment variable:"
echo "     * NEXT_PUBLIC_API_URL=https://your-backend-app.onrender.com"
echo ""
echo "4. 🔧 Environment Variables:"
echo "   - Get your Google Gemini API key from https://makersuite.google.com/app/apikey"
echo "   - Set up Supabase database and get credentials"
echo "   - Update the API URL in lib/api.ts with your actual Render URL"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT.md"
echo ""
print_success "Happy deploying! 🚀" 