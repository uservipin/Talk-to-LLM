import streamlit as st
import os
import json
import pandas as pd
from PIL import Image
import io
import base64
from typing import Dict, Any, List
import requests
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="AI Multi-Modal Assistant",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .model-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .input-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px solid #e9ecef;
    }
    .output-section {
        background: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px solid #28a745;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

class AIModelManager:
    def __init__(self):
        self.models = {
            "Free Models": {
                "Llama 2 (7B)": {
                    "type": "llama",
                    "endpoint": "https://api.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf",
                    "api_key_required": False,
                    "description": "Open source large language model by Meta"
                },
                "Gemini Pro": {
                    "type": "gemini",
                    "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro",
                    "api_key_required": True,
                    "description": "Google's multimodal AI model"
                },
                "GPT-3.5 Turbo": {
                    "type": "openai",
                    "endpoint": "https://api.openai.com/v1/chat/completions",
                    "api_key_required": True,
                    "description": "OpenAI's GPT-3.5 model"
                }
            },
            "Paid Models": {
                "GPT-4": {
                    "type": "openai",
                    "endpoint": "https://api.openai.com/v1/chat/completions",
                    "api_key_required": True,
                    "description": "OpenAI's most advanced model"
                },
                "Claude 3": {
                    "type": "anthropic",
                    "endpoint": "https://api.anthropic.com/v1/messages",
                    "api_key_required": True,
                    "description": "Anthropic's Claude 3 model"
                },
                "Gemini Ultra": {
                    "type": "gemini",
                    "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-ultra",
                    "api_key_required": True,
                    "description": "Google's most advanced Gemini model"
                }
            }
        }
    
    def get_available_models(self) -> Dict[str, Dict]:
        return self.models
    
    def process_with_model(self, model_name: str, input_data: Dict[str, Any], 
                          output_mode: str, api_key: str = None) -> Dict[str, Any]:
        """Process input with selected model"""
        
        # Find the model configuration
        model_config = None
        for category, models in self.models.items():
            if model_name in models:
                model_config = models[model_name]
                break
        
        if not model_config:
            return {"error": "Model not found"}
        
        # Simulate API call (in real implementation, you'd make actual API calls)
        response = self._simulate_api_call(model_config, input_data, output_mode)
        return response
    
    def _simulate_api_call(self, model_config: Dict, input_data: Dict, output_mode: str) -> Dict:
        """Simulate API call to different models"""
        
        prompt = input_data.get("text", "")
        image = input_data.get("image")
        file_content = input_data.get("file_content")
        
        # Create a comprehensive response based on input type and model
        response = {
            "model": model_config["type"],
            "timestamp": datetime.now().isoformat(),
            "input_type": "text" if not image and not file_content else "multimodal",
            "output_mode": output_mode
        }
        
        if output_mode == "brief":
            response["content"] = f"Brief response from {model_config['type']}: {prompt[:100]}..."
            response["summary"] = "This is a concise summary of the analysis."
        else:
            response["content"] = f"""
            Detailed Analysis from {model_config['type']}:
            
            Input Analysis:
            - Text: {prompt}
            - Has Image: {'Yes' if image else 'No'}
            - Has File: {'Yes' if file_content else 'No'}
            
            Comprehensive Response:
            This is a detailed analysis of your input. The model has processed the information
            and provided insights based on the context and requirements.
            
            Key Points:
            1. Input processing completed successfully
            2. Model-specific analysis performed
            3. Context-aware response generated
            4. Recommendations provided
            
            Technical Details:
            - Model: {model_config['type']}
            - Processing Time: ~2.5 seconds
            - Confidence Score: 0.92
            - Tokens Used: 1,247
            """
        
        return response

class FileProcessor:
    def __init__(self):
        self.supported_extensions = {
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
            'document': ['.pdf', '.txt', '.doc', '.docx'],
            'excel': ['.xlsx', '.xls', '.csv'],
            'python': ['.py']
        }
    
    def process_file(self, uploaded_file) -> Dict[str, Any]:
        """Process uploaded file and extract content"""
        if uploaded_file is None:
            return {"error": "No file uploaded"}
        
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        file_info = {
            "filename": uploaded_file.name,
            "size": uploaded_file.size,
            "type": self._get_file_type(file_extension),
            "extension": file_extension
        }
        
        try:
            if file_info["type"] == "image":
                return self._process_image(uploaded_file, file_info)
            elif file_info["type"] == "excel":
                return self._process_excel(uploaded_file, file_info)
            elif file_info["type"] == "python":
                return self._process_python(uploaded_file, file_info)
            elif file_info["type"] == "document":
                return self._process_document(uploaded_file, file_info)
            else:
                return {"error": f"Unsupported file type: {file_extension}"}
        except Exception as e:
            return {"error": f"Error processing file: {str(e)}"}
    
    def _get_file_type(self, extension: str) -> str:
        for file_type, extensions in self.supported_extensions.items():
            if extension in extensions:
                return file_type
        return "unknown"
    
    def _process_image(self, file, file_info: Dict) -> Dict[str, Any]:
        image = Image.open(file)
        file_info["dimensions"] = image.size
        file_info["mode"] = image.mode
        
        # Convert to base64 for display
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        file_info["base64"] = img_str
        
        return file_info
    
    def _process_excel(self, file, file_info: Dict) -> Dict[str, Any]:
        try:
            if file_info["extension"] == ".csv":
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            
            file_info["rows"] = len(df)
            file_info["columns"] = len(df.columns)
            file_info["column_names"] = df.columns.tolist()
            file_info["data_preview"] = df.head().to_dict()
            file_info["summary_stats"] = df.describe().to_dict()
            
            return file_info
        except Exception as e:
            return {"error": f"Error reading Excel file: {str(e)}"}
    
    def _process_python(self, file, file_info: Dict) -> Dict[str, Any]:
        content = file.read().decode('utf-8')
        file_info["lines"] = len(content.split('\n'))
        file_info["content"] = content
        file_info["functions"] = self._extract_functions(content)
        
        return file_info
    
    def _process_document(self, file, file_info: Dict) -> Dict[str, Any]:
        content = file.read().decode('utf-8')
        file_info["lines"] = len(content.split('\n'))
        file_info["words"] = len(content.split())
        file_info["content"] = content[:1000] + "..." if len(content) > 1000 else content
        
        return file_info
    
    def _extract_functions(self, code: str) -> List[str]:
        """Extract function names from Python code"""
        import re
        function_pattern = r'def\s+(\w+)\s*\('
        return re.findall(function_pattern, code)

def main():
    # Initialize managers
    model_manager = AIModelManager()
    file_processor = FileProcessor()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Multi-Modal Assistant</h1>', unsafe_allow_html=True)
    
    # Sidebar for model selection and settings
    with st.sidebar:
        st.markdown("## 🎛️ Model Configuration")
        
        # Model selection
        model_category = st.selectbox(
            "Select Model Category",
            ["Free Models", "Paid Models"]
        )
        
        available_models = model_manager.get_available_models()[model_category]
        selected_model = st.selectbox(
            "Choose AI Model",
            list(available_models.keys()),
            format_func=lambda x: f"{x} - {available_models[x]['description']}"
        )
        
        # API Key input
        api_key = st.text_input(
            "API Key (if required)",
            type="password",
            help="Enter your API key for the selected model"
        )
        
        # Output mode selection
        output_mode = st.radio(
            "Output Mode",
            ["brief", "detailed"],
            format_func=lambda x: "Brief" if x == "brief" else "Detailed"
        )
        
        # Settings
        st.markdown("## ⚙️ Settings")
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
        max_tokens = st.slider("Max Tokens", 100, 4000, 1000, 100)
        
        # Session info
        st.markdown("## 📊 Session Info")
        if "session_count" not in st.session_state:
            st.session_state.session_count = 0
        st.metric("Requests", st.session_state.session_count)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown("## 📥 Input")
        
        # Input type selection
        input_type = st.radio(
            "Select Input Type",
            ["Text", "Image", "File Upload", "Multi-Modal"]
        )
        
        # Text input
        if input_type in ["Text", "Multi-Modal"]:
            text_input = st.text_area(
                "Enter your prompt",
                height=150,
                placeholder="Describe what you want the AI to help you with..."
            )
        
        # Image input
        if input_type in ["Image", "Multi-Modal"]:
            uploaded_image = st.file_uploader(
                "Upload Image",
                type=['png', 'jpg', 'jpeg', 'gif'],
                help="Upload an image for analysis"
            )
        
        # File upload
        if input_type in ["File Upload", "Multi-Modal"]:
            uploaded_file = st.file_uploader(
                "Upload File",
                type=['pdf', 'txt', 'doc', 'docx', 'xlsx', 'xls', 'csv', 'py'],
                help="Upload documents, Excel files, or Python code"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="output-section">', unsafe_allow_html=True)
        st.markdown("##  Output")
        
        # Process button
        if st.button("🚀 Process with AI", use_container_width=True):
            if "session_count" not in st.session_state:
                st.session_state.session_count = 0
            
            # Prepare input data
            input_data = {"text": text_input if input_type in ["Text", "Multi-Modal"] else ""}
            
            # Process image
            if input_type in ["Image", "Multi-Modal"] and uploaded_image:
                image_info = file_processor.process_file(uploaded_image)
                if "error" not in image_info:
                    input_data["image"] = image_info
            
            # Process file
            if input_type in ["File Upload", "Multi-Modal"] and uploaded_file:
                file_info = file_processor.process_file(uploaded_file)
                if "error" not in file_info:
                    input_data["file_content"] = file_info
            
            # Process with AI model
            with st.spinner(" Processing with AI..."):
                result = model_manager.process_with_model(
                    selected_model, input_data, output_mode, api_key
                )
            
            # Display results
            if "error" not in result:
                st.session_state.session_count += 1
                
                # Display model info
                st.info(f"**Model:** {result['model']} | **Mode:** {result['output_mode']}")
                
                # Display content
                st.markdown("### Response:")
                st.write(result["content"])
                
                # Display input analysis
                if input_data.get("image"):
                    st.markdown("### Image Analysis:")
                    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
                
                if input_data.get("file_content"):
                    st.markdown("### File Analysis:")
                    file_info = input_data["file_content"]
                    st.json(file_info)
                
                # Add to session history
                if "history" not in st.session_state:
                    st.session_state.history = []
                
                st.session_state.history.append({
                    "timestamp": result["timestamp"],
                    "model": result["model"],
                    "input": input_data,
                    "output": result["content"]
                })
            else:
                st.error(f"Error: {result['error']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # History section
    if "history" in st.session_state and st.session_state.history:
        st.markdown("##  Session History")
        
        for i, entry in enumerate(reversed(st.session_state.history[-5:])):  # Show last 5 entries
            with st.expander(f"Request {len(st.session_state.history) - i} - {entry['model']} ({entry['timestamp'][:19]})"):
                st.write("**Input:**", entry["input"].get("text", "No text input"))
                st.write("**Output:**", entry["output"])
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <p>🤖 AI Multi-Modal Assistant | Built with Streamlit | Support for Llama, GPT, Gemini</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
