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
import uuid
from auth import UserAuth

# test update

# Page configuration
# Check conflict

# check commit

st.set_page_config(
    page_title="AI Assistant Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern, clean design with improved UI
st.markdown("""
<style>
    /* Global styles */
    .main {
        padding: 0;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Header styles */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 0;
        margin-bottom: 2rem;
        border-radius: 0 0 30px 30px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        pointer-events: none;
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        color: white;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .header-subtitle {
        text-align: center;
        color: rgba(255,255,255,0.95);
        font-size: 1.2rem;
        margin-top: 0.5rem;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }
    
    /* Card styles */
    .card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    .card-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    /* Button styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1rem 2.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    
    /* Secondary button styles */
    .secondary-button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.4);
    }
    
    .secondary-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(240, 147, 251, 0.6);
    }
    
    /* Input styles */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #e9ecef;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.9);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        background: white;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 15px;
        border: 2px solid #e9ecef;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.9);
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        background: white;
    }
    
    /* Sidebar styles */
    .css-1d391kg {
        background: rgba(248, 249, 250, 0.95);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Success/Error messages */
    .success-message {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(212, 237, 218, 0.3);
    }
    
    .error-message {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(248, 215, 218, 0.3);
    }
    
    /* Model selection styles */
    .model-option {
        background: rgba(248, 249, 250, 0.9);
        border: 2px solid #e9ecef;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.8rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
    }
    
    .model-option:hover {
        border-color: #667eea;
        background: rgba(240, 242, 255, 0.9);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.15);
    }
    
    .model-option.selected {
        border-color: #667eea;
        background: linear-gradient(135deg, #f0f2ff 0%, #e6e9ff 100%);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    /* Feedback button styles */
    .feedback-container {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 1.5rem 0;
        padding: 1.5rem;
        background: rgba(248, 249, 250, 0.9);
        border-radius: 15px;
        border: 1px solid #e9ecef;
        backdrop-filter: blur(5px);
    }
    
    .feedback-button {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 50px;
        padding: 0.8rem 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .feedback-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .feedback-button.thumbs-up {
        border-color: #28a745;
        color: #28a745;
    }
    
    .feedback-button.thumbs-up:hover {
        background: #28a745;
        color: white;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
    }
    
    .feedback-button.thumbs-down {
        border-color: #dc3545;
        color: #dc3545;
    }
    
    .feedback-button.thumbs-down:hover {
        background: #dc3545;
        color: white;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
    }
    
    /* Tab styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px 10px 0 0;
        border: 1px solid #e9ecef;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        .card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

class AIModelManager:
    def __init__(self):
        self.models = {
            "Free Models": {
                "Demo Model": {
                    "type": "demo",
                    "endpoint": "local",
                    "api_key_required": False,
                    "description": "Local demo model - no API key needed",
                    "icon": "🎯",
                    "max_tokens": 1000,
                    "temperature": 0.7
                },
                "GPT-3.5 Turbo (Free Tier)": {
                    "type": "openai",
                    "endpoint": "https://api.openai.com/v1/chat/completions",
                    "api_key_required": True,
                    "description": "OpenAI's free tier - requires API key",
                    "icon": "🧠",
                    "max_tokens": 1000,
                    "temperature": 0.7
                },
                "Gemini Pro (Free Tier)": {
                    "type": "gemini",
                    "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro",
                    "api_key_required": True,
                    "description": "Google's free tier - requires API key",
                    "icon": "🤖",
                    "max_tokens": 1000,
                    "temperature": 0.7
                },
                "Claude 3 Haiku (Free)": {
                    "type": "anthropic",
                    "endpoint": "https://api.anthropic.com/v1/messages",
                    "api_key_required": True,
                    "description": "Anthropic's fastest Claude model",
                    "icon": "🎭",
                    "max_tokens": 1000,
                    "temperature": 0.7
                }
            },
            "Paid Models": {
                "GPT-4": {
                    "type": "openai",
                    "endpoint": "https://api.openai.com/v1/chat/completions",
                    "api_key_required": True,
                    "description": "OpenAI's most advanced model",
                    "icon": "🚀",
                    "max_tokens": 4000,
                    "temperature": 0.7
                },
                "GPT-4 Turbo": {
                    "type": "openai",
                    "endpoint": "https://api.openai.com/v1/chat/completions",
                    "api_key_required": True,
                    "description": "OpenAI's latest GPT-4 model",
                    "icon": "⚡",
                    "max_tokens": 4000,
                    "temperature": 0.7
                },
                "Claude 3 Sonnet": {
                    "type": "anthropic",
                    "endpoint": "https://api.anthropic.com/v1/messages",
                    "api_key_required": True,
                    "description": "Anthropic's balanced Claude model",
                    "icon": "🎭",
                    "max_tokens": 4000,
                    "temperature": 0.7
                },
                "Claude 3 Opus": {
                    "type": "anthropic",
                    "endpoint": "https://api.anthropic.com/v1/messages",
                    "api_key_required": True,
                    "description": "Anthropic's most capable Claude model",
                    "icon": "👑",
                    "max_tokens": 4000,
                    "temperature": 0.7
                },
                "Gemini Ultra": {
                    "type": "gemini",
                    "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-ultra",
                    "api_key_required": True,
                    "description": "Google's most advanced Gemini model",
                    "icon": "⭐",
                    "max_tokens": 4000,
                    "temperature": 0.7
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
            "model_name": model_config.get("icon", "🤖") + " " + model_config.get("type", "Unknown"),
            "timestamp": datetime.now().isoformat(),
            "input_type": "text" if not image and not file_content else "multimodal",
            "output_mode": output_mode,
            "response_id": str(uuid.uuid4())  # Unique ID for feedback tracking
        }
        
        if output_mode == "brief":
            response["content"] = f"**{model_config.get('icon', '🤖')} Brief Response:**\n\n{prompt[:100]}..."
            response["summary"] = "This is a concise summary of the analysis."
        else:
            response["content"] = f"""
            ## {model_config.get('icon', '🤖')} Detailed Analysis
            
            **Input Analysis:**
            - Text: {prompt}
            - Has Image: {'Yes' if image else 'No'}
            - Has File: {'Yes' if file_content else 'No'}
            
            **Comprehensive Response:**
            This is a detailed analysis of your input. The model has processed the information
            and provided insights based on the context and requirements.
            
            **Key Points:**
            1. Input processing completed successfully
            2. Model-specific analysis performed
            3. Context-aware response generated
            4. Recommendations provided
            
            **Technical Details:**
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

def login_page():
    """Display login/register page"""
    auth = UserAuth()
    
    st.markdown("""
        <div class="header-container">
            <h1 class="header-title">🤖 AI Assistant Pro</h1>
            <p class="header-subtitle">Your Personal AI Companion</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h2 class="card-title">🔐 Welcome Back</h2>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.markdown("### Sign In")
            email = st.text_input("Email Address", placeholder="your.email@gmail.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_login1, col_login2 = st.columns(2)
            with col_login1:
                if st.button("Sign In", use_container_width=True):
                    if email and password:
                        success, result = auth.login_user(email, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.user_email = email
                            st.session_state.session_id = result
                            st.session_state.user_info = auth.get_user_info(email)
                            st.rerun()
                        else:
                            st.error(result)
                    else:
                        st.error("Please enter both email and password")
            
            with col_login2:
                if st.button("Forgot Password?", use_container_width=True):
                    st.info("Please contact support to reset your password.")
        
        with tab2:
            st.markdown("### Create New Account")
            new_email = st.text_input("Email Address", key="reg_email", placeholder="your.email@gmail.com")
            name = st.text_input("Full Name", key="reg_name", placeholder="Your Full Name")
            new_password = st.text_input("Password", type="password", key="reg_password", placeholder="Create a password (min 6 characters)")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Confirm your password")
            
            if st.button("Create Account", use_container_width=True):
                if new_email and name and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters long")
                    else:
                        success, result = auth.register_user(new_email, name, new_password)
                        if success:
                            st.success("Account created successfully! Please login.")
                        else:
                            st.error(result)
                else:
                    st.error("Please fill in all fields")
        
        st.markdown('</div>', unsafe_allow_html=True)

def feedback_component(response_id: str, user_email: str):
    """Display feedback buttons for AI responses"""
    auth = UserAuth()
    
    # Check if user has already given feedback for this response
    existing_feedback = auth.get_user_feedback(user_email)
    user_feedback = next((f for f in existing_feedback if f.get("response_id") == response_id), None)
    
    st.markdown("---")
    st.markdown("### 💬 How was this response?")
    
    # Show current feedback status if exists
    if user_feedback:
        if user_feedback["feedback"] == "positive":
            st.success("✅ You marked this response as helpful")
        else:
            st.error("❌ You marked this response as not helpful")
        return
    
    # Feedback buttons with better styling
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        feedback_container = st.container()
        
        with feedback_container:
            col_thumbs_up, col_thumbs_down = st.columns(2)
            
            with col_thumbs_up:
                if st.button(
                    "👍 Helpful", 
                    key=f"thumbs_up_{response_id}", 
                    use_container_width=True,
                    help="Mark this response as helpful"
                ):
                    feedback_entry = {
                        "response_id": response_id,
                        "feedback": "positive",
                        "timestamp": datetime.now().isoformat(),
                        "user_email": user_email
                    }
                    auth.save_user_feedback(user_email, feedback_entry)
                    st.success("🎉 Thank you for your feedback! This helps us improve.")
                    st.rerun()
            
            with col_thumbs_down:
                if st.button(
                    "👎 Not Helpful", 
                    key=f"thumbs_down_{response_id}", 
                    use_container_width=True,
                    help="Mark this response as not helpful"
                ):
                    feedback_entry = {
                        "response_id": response_id,
                        "feedback": "negative",
                        "timestamp": datetime.now().isoformat(),
                        "user_email": user_email
                    }
                    auth.save_user_feedback(user_email, feedback_entry)
                    st.error("📝 Thank you for your feedback! We'll work to improve.")
                    st.rerun()

def show_feedback_analytics(auth: UserAuth, user_email: str):
    """Display feedback analytics for the user"""
    feedback_data = auth.get_user_feedback(user_email)
    
    if not feedback_data:
        st.info("No feedback data available yet. Start chatting to provide feedback!")
        return
    
    # Calculate statistics
    total_feedback = len(feedback_data)
    positive_feedback = len([f for f in feedback_data if f.get("feedback") == "positive"])
    negative_feedback = len([f for f in feedback_data if f.get("feedback") == "negative"])
    satisfaction_rate = (positive_feedback / total_feedback * 100) if total_feedback > 0 else 0
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Feedback", total_feedback)
    
    with col2:
        st.metric("👍 Helpful", positive_feedback)
    
    with col3:
        st.metric("👎 Not Helpful", negative_feedback)
    
    with col4:
        st.metric("Satisfaction Rate", f"{satisfaction_rate:.1f}%")
    
    # Create feedback chart
    if total_feedback > 0:
        feedback_df = pd.DataFrame([
            {"Feedback": "Helpful", "Count": positive_feedback, "Color": "#28a745"},
            {"Feedback": "Not Helpful", "Count": negative_feedback, "Color": "#dc3545"}
        ])
        
        fig = px.bar(feedback_df, x="Feedback", y="Count", 
                    color="Feedback", color_discrete_map={
                        "Helpful": "#28a745",
                        "Not Helpful": "#dc3545"
                    })
        fig.update_layout(
            title="Your Feedback Distribution",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Show recent feedback
    st.markdown("### Recent Feedback")
    recent_feedback = feedback_data[-10:]  # Last 10 feedback entries
    
    for feedback in reversed(recent_feedback):
        with st.expander(f"Feedback on {feedback.get('timestamp', '')[:19]}"):
            st.write(f"**Response ID:** {feedback.get('response_id', 'Unknown')}")
            st.write(f"**Feedback:** {'👍 Helpful' if feedback.get('feedback') == 'positive' else '👎 Not Helpful'}")
            st.write(f"**Date:** {feedback.get('timestamp', '')}")

def main_app():
    """Main application after login"""
    auth = UserAuth()
    model_manager = AIModelManager()
    file_processor = FileProcessor()
    
    # Header with user info
    user_info = st.session_state.user_info
    st.markdown(f"""
        <div class="header-container">
            <h1 class="header-title">🤖 AI Assistant Pro</h1>
            <p class="header-subtitle">Welcome back, {user_info['name']}! ({user_info['email']})</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for navigation and settings
    with st.sidebar:
        st.markdown("## 🎛️ AI Model Settings")
        
        # Model selection with better UI
        model_category = st.selectbox(
            "📂 Model Category",
            ["Free Models", "Paid Models"],
            help="Choose between free and paid AI models"
        )
        
        available_models = model_manager.get_available_models()[model_category]
        
        # Display model options with descriptions
        st.markdown("### 🤖 Available Models")
        for model_name, model_config in available_models.items():
            with st.expander(f"{model_config['icon']} {model_name}", expanded=False):
                st.write(f"**Description:** {model_config['description']}")
                st.write(f"**Type:** {model_config['type'].title()}")
                st.write(f"**API Key:** {'Required' if model_config['api_key_required'] else 'Not Required'}")
                st.write(f"**Max Tokens:** {model_config.get('max_tokens', 'N/A')}")
        
        selected_model = st.selectbox(
            "🎯 Select Model",
            list(available_models.keys()),
            help="Choose the AI model you want to use"
        )
        
        # Get selected model config
        selected_model_config = available_models[selected_model]
        
        # Display selected model info
        st.markdown("### 📋 Selected Model")
        st.info(f"""
        **{selected_model_config['icon']} {selected_model}**
        
        {selected_model_config['description']}
        
        **Type:** {selected_model_config['type'].title()}
        **API Key:** {'Required' if selected_model_config['api_key_required'] else 'Not Required'}
        """)
        
        # API Key input - only show if required
        if selected_model_config["api_key_required"]:
            api_key = st.text_input(
                "🔑 API Key",
                type="password",
                help="Required for this model"
            )
            if not api_key:
                st.warning("⚠️ API key required for this model")
        else:
            api_key = None
            st.success("✅ No API key needed")
        
        # Output mode
        st.markdown("### ⚙️ Response Settings")
        output_mode = st.radio(
            "Output Style",
            ["brief", "detailed"],
            format_func=lambda x: "Quick Response" if x == "brief" else "Detailed Analysis",
            help="Choose response length and detail level"
        )
        
        # Advanced settings
        st.markdown("### 🔧 Advanced Settings")
        temperature = st.slider(
            "Creativity Level", 
            0.0, 2.0, 
            selected_model_config.get("temperature", 0.7), 
            0.1,
            help="Higher values = more creative, Lower values = more focused"
        )
        max_tokens = st.slider(
            "Response Length", 
            100, 4000, 
            selected_model_config.get("max_tokens", 1000), 
            100,
            help="Maximum number of tokens in the response"
        )
        
        # User actions
        st.markdown("## 👤 Account")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 History", use_container_width=True):
                st.session_state.show_history = True
                st.session_state.show_feedback = False
        
        with col2:
            if st.button("💬 Feedback", use_container_width=True):
                st.session_state.show_feedback = True
                st.session_state.show_history = False
        
        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
    
    # Main content area
    if st.session_state.get("show_history", False):
        show_history_page(auth)
    elif st.session_state.get("show_feedback", False):
        show_feedback_analytics_page(auth)
    else:
        show_chat_page(model_manager, file_processor, selected_model, selected_model_config, api_key, output_mode)

def show_history_page(auth):
    """Display user's chat history"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="card-title">📊 Your Chat History</h2>', unsafe_allow_html=True)
    
    history = auth.get_user_history(st.session_state.user_email)
    
    if not history:
        st.info("No chat history found. Start a conversation to see your history here!")
    else:
        for i, entry in enumerate(reversed(history[-20:])):  # Show last 20 entries
            with st.expander(f"Chat {len(history) - i} - {entry.get('model_name', 'Unknown')} ({entry.get('timestamp', '')[:19]})"):
                st.write("**Input:**", entry.get("input", {}).get("text", "No text input"))
                st.write("**Output:**", entry.get("output", "No output"))
                
                # Show feedback if available
                feedback_data = auth.get_user_feedback(st.session_state.user_email)
                response_feedback = next((f for f in feedback_data if f.get("response_id") == entry.get("response_id")), None)
                if response_feedback:
                    if response_feedback["feedback"] == "positive":
                        st.success("✅ Marked as helpful")
                    else:
                        st.error("❌ Marked as not helpful")
    
    if st.button("← Back to Chat"):
        st.session_state.show_history = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_feedback_analytics_page(auth):
    """Display feedback analytics page"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="card-title">💬 Feedback Analytics</h2>', unsafe_allow_html=True)
    
    show_feedback_analytics(auth, st.session_state.user_email)
    
    if st.button("← Back to Chat"):
        st.session_state.show_feedback = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_chat_page(model_manager, file_processor, selected_model, selected_model_config, api_key, output_mode):
    """Main chat interface"""
    
    # Input section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<h2 class="card-title">💬 Chat with {selected_model_config.get("icon", "🤖")} {selected_model}</h2>', unsafe_allow_html=True)
    
    # Model info display
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("Model Type", selected_model_config["type"].title())
    with col_info2:
        st.metric("API Key", "Required" if selected_model_config["api_key_required"] else "Not Required")
    with col_info3:
        st.metric("Output Mode", "Quick" if output_mode == "brief" else "Detailed")
    
    st.markdown("---")
    
    # Input type selection with better UI
    st.markdown("### 📝 Input Options")
    input_type = st.radio(
        "Choose Input Type",
        ["Text", "Image", "File", "Multi-Modal"],
        horizontal=True,
        help="Select how you want to interact with the AI"
    )
    
    # Text input
    if input_type in ["Text", "Multi-Modal"]:
        text_input = st.text_area(
            "Your Message",
            height=150,
            placeholder="What would you like to ask the AI? Be specific and detailed for better responses...",
            help="Enter your question or prompt here"
        )
    
    # File uploads with better organization
    if input_type in ["Image", "File", "Multi-Modal"]:
        st.markdown("### 📎 File Upload")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if input_type in ["Image", "Multi-Modal"]:
                uploaded_image = st.file_uploader(
                    "📷 Upload Image",
                    type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'],
                    help="Upload an image for analysis (max 10MB)"
                )
                if uploaded_image:
                    st.image(uploaded_image, caption="Preview", use_column_width=True)
        
        with col2:
            if input_type in ["File", "Multi-Modal"]:
                uploaded_file = st.file_uploader(
                    "📄 Upload File",
                    type=['pdf', 'txt', 'doc', 'docx', 'xlsx', 'xls', 'csv', 'py', 'json', 'xml'],
                    help="Upload documents, spreadsheets, or code files (max 10MB)"
                )
                if uploaded_file:
                    st.success(f"✅ File uploaded: {uploaded_file.name}")
    
    # Process button with validation
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        if st.button("🚀 Send to AI", use_container_width=True, type="primary"):
            # Validate input
            has_text = text_input and text_input.strip() if input_type in ["Text", "Multi-Modal"] else False
            has_image = uploaded_image is not None if input_type in ["Image", "Multi-Modal"] else False
            has_file = uploaded_file is not None if input_type in ["File", "Multi-Modal"] else False
            
            if not has_text and not has_image and not has_file:
                st.error("⚠️ Please provide some input (text, image, or file)")
            elif selected_model_config["api_key_required"] and not api_key:
                st.error("⚠️ API key is required for this model")
            else:
                # Prepare input data
                input_data = {"text": text_input.strip() if has_text else ""}
                
                # Process image
                if has_image:
                    with st.spinner("Processing image..."):
                        image_info = file_processor.process_file(uploaded_image)
                        if "error" not in image_info:
                            input_data["image"] = image_info
                        else:
                            st.error(f"Image processing error: {image_info['error']}")
                            return
                
                # Process file
                if has_file:
                    with st.spinner("Processing file..."):
                        file_info = file_processor.process_file(uploaded_file)
                        if "error" not in file_info:
                            input_data["file_content"] = file_info
                        else:
                            st.error(f"File processing error: {file_info['error']}")
                            return
                
                # Process with AI model
                with st.spinner(f"🤖 {selected_model_config.get('icon', '🤖')} {selected_model} is thinking..."):
                    result = model_manager.process_with_model(
                        selected_model, input_data, output_mode, api_key
                    )
                
                # Display results
                if "error" not in result:
                    # Save to user history
                    auth = UserAuth()
                    history_entry = {
                        "timestamp": result["timestamp"],
                        "model_name": result["model_name"],
                        "input": input_data,
                        "output": result["content"],
                        "response_id": result["response_id"]
                    }
                    auth.save_user_history(st.session_state.user_email, history_entry)
                    
                    # Display response in a nice container
                    st.markdown("---")
                    st.markdown("### 🤖 AI Response")
                    
                    # Response container with styling
                    response_container = st.container()
                    with response_container:
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                            padding: 1.5rem;
                            border-radius: 15px;
                            border-left: 5px solid #667eea;
                            margin: 1rem 0;
                        ">
                            {result["content"]}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Display feedback component
                    feedback_component(result["response_id"], st.session_state.user_email)
                    
                    # Display file analysis if present
                    if input_data.get("image"):
                        st.markdown("### 📷 Image Analysis")
                        col_img1, col_img2 = st.columns([1, 2])
                        with col_img1:
                            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
                        with col_img2:
                            st.json(input_data["image"])
                    
                    if input_data.get("file_content"):
                        st.markdown("### 📄 File Analysis")
                        with st.expander("📋 View File Details", expanded=False):
                            st.json(input_data["file_content"])
                else:
                    st.error(f"❌ Error: {result['error']}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    # Check if user is logged in
    if st.session_state.logged_in:
        main_app()
    else:
        login_page()

if __name__ == "__main__":
    main()
