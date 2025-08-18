# 🤖 AI Multi-Modal Assistant

A comprehensive Streamlit application that allows you to interact with various AI models (free and paid) using multiple input types including text, images, documents, Excel files, and Python code.

## ✨ Features

### 🎯 Multi-Model Support
- **Free Models**: Llama 2, Gemini Pro, GPT-3.5 Turbo
- **Paid Models**: GPT-4, Claude 3, Gemini Ultra

### �� Multi-Modal Input
- **Text**: Natural language prompts
- **Images**: JPG, PNG, GIF, BMP, TIFF
- **Documents**: PDF, TXT, DOC, DOCX
- **Excel Files**: XLSX, XLS, CSV
- **Python Code**: .py files with syntax analysis

### ��️ Output Modes
- **Brief**: Concise, to-the-point responses
- **Detailed**: Comprehensive analysis with explanations

### 🎨 Modern UI
- Beautiful gradient design
- Responsive layout
- Real-time processing indicators
- Session history tracking

## �� Quick Start

### 1. Installation

```bash
# Clone or navigate to the project directory
cd "Talk to LLM"

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file in the project directory:

```env
# OpenAI API Keys
OPENAI_API_KEY=your_openai_api_key_here

# Google Gemini API Key
GOOGLE_API_KEY=your_google_api_key_here

# Anthropic API Key
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Hugging Face API Key (for Llama)
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## �� Usage Guide

### 1. Model Selection
- Choose between "Free Models" and "Paid Models" in the sidebar
- Select your preferred AI model
- Enter API key if required

### 2. Input Configuration
- Select input type: Text, Image, File Upload, or Multi-Modal
- Enter your prompt or upload files
- Adjust settings like temperature and max tokens

### 3. Processing
- Click "Process with AI" to start analysis
- View real-time processing status
- Get results in your chosen output mode

### 4. Output Analysis
- **Brief Mode**: Quick insights and summaries
- **Detailed Mode**: Comprehensive analysis with technical details
- Session history for tracking previous requests

## �� Configuration

### Model Settings
- **Temperature**: Controls response creativity (0.0-2.0)
- **Max Tokens**: Maximum response length
- **Output Mode**: Brief or detailed responses

### File Processing
- **Supported Formats**: See features section above
- **Max File Size**: 10MB per file
- **Batch Processing**: Multiple files in one session

## 🛠️ Technical Architecture

### Core Components
- **AIModelManager**: Handles model selection and API calls
- **FileProcessor**: Processes different file types
- **ModelHandlers**: Specific implementations for each AI provider
- **Streamlit UI**: Modern, responsive interface

### Supported AI Providers
- OpenAI (GPT-3.5, GPT-4)
- Google (Gemini Pro, Gemini Ultra)
- Anthropic (Claude 3)
- Meta (Llama 2 via Hugging Face)

## �� Security & Privacy

- API keys are stored securely in environment variables
- No data is stored permanently on the server
- File processing is done locally
- Session data is cleared when the app is restarted

## 🚧 Limitations

- Some models require paid API keys
- File size limits apply
- Processing speed depends on model and input size
- Internet connection required for API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the documentation above
2. Review the error messages in the app
3. Ensure your API keys are correctly configured
4. Verify your internet connection

## 🔄 Updates

Stay updated with the latest features:
- Regular model updates
- New file format support
- UI/UX improvements
- Performance optimizations
