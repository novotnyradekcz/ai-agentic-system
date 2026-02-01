#!/bin/bash
# Quick Start Script for RAG Pipeline

echo "========================================="
echo "RAG Pipeline - Quick Start"
echo "========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/.installed" ]; then
    echo "Installing dependencies (this may take a few minutes)..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/.installed
    echo "✓ Dependencies installed"
else
    echo "✓ Dependencies already installed"
fi

# Check for ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo ""
    echo "⚠️  WARNING: ffmpeg not found!"
    echo "ffmpeg is required for audio/video processing."
    echo ""
    echo "Install it with:"
    echo "  macOS:   brew install ffmpeg"
    echo "  Ubuntu:  sudo apt-get install ffmpeg"
    echo "  Windows: Download from https://ffmpeg.org/download.html"
    echo ""
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  WARNING: .env file not found!"
    echo "Please create a .env file with your API keys:"
    echo "  cp .env.example .env"
    echo "  # Then edit .env to add your keys"
    echo ""
fi

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Add your PDF/audio files to the data/ directory"
echo "2. Configure your API keys in .env file"
echo "3. Run the pipeline:"
echo ""
echo "   # Process all files:"
echo "   python run_pipeline.py"
echo ""
echo "   # Ask a question:"
echo "   python run_pipeline.py --query 'Your question?'"
echo ""
echo "   # Interactive mode:"
echo "   python run_pipeline.py --interactive"
echo ""
echo "========================================="
