#!/bin/bash

# Jarvis Phase 1 - Automatic Setup Script
# Run: bash setup.sh

set -e

echo "🧠 Jarvis Phase 1 - Setup Script"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python $PYTHON_VERSION found"

# Check Node
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js not found. Frontend setup will be skipped."
    echo "   Install from: https://nodejs.org"
    SKIP_FRONTEND=1
else
    NODE_VERSION=$(node -v)
    echo "✓ Node $NODE_VERSION found"
fi

echo ""
echo "📁 Setting up project structure..."
echo ""

# Backend setup
echo "🔧 Setting up Backend..."
cd backend

if [ ! -f ".env" ]; then
    echo "  Creating .env file..."
    cp .env.example .env
    echo "  ⚠️  IMPORTANT: Edit backend/.env and add your API keys:"
    echo "     MEM0_API_KEY=your_key_here"
    echo "     ANTHROPIC_API_KEY=your_key_here"
else
    echo "  ✓ .env already exists"
fi

if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv venv
    echo "  ✓ venv created"
else
    echo "  ✓ venv already exists"
fi

echo "  Activating venv..."
source venv/bin/activate

echo "  Installing dependencies..."
pip install -q -r ../requirements.txt
echo "  ✓ Dependencies installed"

cd ..

# Frontend setup
if [ -z "$SKIP_FRONTEND" ]; then
    echo ""
    echo "🎨 Setting up Frontend..."
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        echo "  Installing npm packages..."
        npm install -q
        echo "  ✓ npm packages installed"
    else
        echo "  ✓ node_modules already exists"
    fi
    
    cd ..
fi

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Edit your API keys:"
echo "   nano backend/.env"
echo ""
echo "2. Start backend:"
echo "   cd backend && source venv/bin/activate && python main.py"
echo ""
if [ -z "$SKIP_FRONTEND" ]; then
    echo "3. Start frontend (in another terminal):"
    echo "   cd frontend && npm run dev"
    echo ""
    echo "4. Open browser:"
    echo "   http://localhost:3000"
else
    echo "3. Install Node.js from https://nodejs.org"
    echo ""
    echo "4. Then start frontend:"
    echo "   cd frontend && npm install && npm run dev"
fi
echo ""
echo "🚀 Happy hacking!"
