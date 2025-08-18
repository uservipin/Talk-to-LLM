#!/bin/bash

# AI Multi-Modal Assistant Launcher
echo "🤖 Starting AI Multi-Modal Assistant..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if requirements are installed
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found. Please ensure you're in the correct directory."
    exit 1
fi

# Install requirements if needed
echo "📦 Installing/updating dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating template..."
    cat > .env << EOF
# OpenAI API Keys
OPENAI_API_KEY=your_openai_api_key_here

# Google Gemini API Key
GOOGLE_API_KEY=your_google_api_key_here

# Anthropic API Key
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Hugging Face API Key (for Llama)
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
EOF
    echo "📝 Please edit .env file with your API keys before running the app."
fi

# Start the application
echo "🚀 Launching Streamlit app..."
streamlit run app.py
