import os
import json
import uuid
import hashlib
import secrets
from datetime import datetime
from typing import Dict, Any, List, Tuple

class UserAuth:
    def __init__(self):
        self.data_dir = "user_data"
        self.users_file = os.path.join(self.data_dir, "users.json")
        self.history_file = os.path.join(self.data_dir, "history.json")
        self.feedback_file = os.path.join(self.data_dir, "feedback.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize data files
        self._init_data_files()
        
        # Load users
        self.users = self._load_users()
    
    def _init_data_files(self):
        """Initialize data files if they don't exist"""
        files_to_init = [
            (self.users_file, {}),
            (self.history_file, {}),
            (self.feedback_file, {})
        ]
        
        for file_path, default_data in files_to_init:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump(default_data, f, indent=2)
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256 with salt"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256((password + salt).encode())
        return f"{salt}${hash_obj.hexdigest()}"
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hashed password"""
        try:
            salt, hash_value = hashed_password.split('$')
            hash_obj = hashlib.sha256((password + salt).encode())
            return hash_obj.hexdigest() == hash_value
        except:
            return False
    
    def _load_users(self) -> Dict[str, Dict]:
        """Load users from JSON file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_users(self):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def _load_history(self) -> Dict[str, List]:
        """Load chat history from JSON file"""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_history(self, history_data: Dict[str, List]):
        """Save chat history to JSON file"""
        with open(self.history_file, 'w') as f:
            json.dump(history_data, f, indent=2)
    
    def _load_feedback(self) -> Dict[str, List]:
        """Load feedback data from JSON file"""
        try:
            with open(self.feedback_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_feedback(self, feedback_data: Dict[str, List]):
        """Save feedback data to JSON file"""
        with open(self.feedback_file, 'w') as f:
            json.dump(feedback_data, f, indent=2)
    
    def register_user(self, email: str, name: str, password: str) -> Tuple[bool, str]:
        """Register a new user"""
        if not email or not name or not password:
            return False, "Email, name, and password are required"
        
        # Simple email validation
        if "@" not in email or "." not in email:
            return False, "Please enter a valid email address"
        
        # Password validation
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        if email in self.users:
            return False, "User already exists"
        
        # Create new user
        user_data = {
            "email": email,
            "name": name,
            "password": self._hash_password(password),
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat()
        }
        
        self.users[email] = user_data
        self._save_users()
        
        return True, "User registered successfully"
    
    def login_user(self, email: str, password: str) -> Tuple[bool, str]:
        """Login a user"""
        if not email or not password:
            return False, "Email and password are required"
        
        if email not in self.users:
            return False, "Invalid email or password"
        
        user = self.users[email]
        
        # Verify password
        if not self._verify_password(password, user.get("password", "")):
            return False, "Invalid email or password"
        
        # Update last login time
        self.users[email]["last_login"] = datetime.now().isoformat()
        self._save_users()
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        return True, session_id
    
    def change_password(self, email: str, current_password: str, new_password: str) -> Tuple[bool, str]:
        """Change user password"""
        if email not in self.users:
            return False, "User not found"
        
        user = self.users[email]
        
        # Verify current password
        if not self._verify_password(current_password, user.get("password", "")):
            return False, "Current password is incorrect"
        
        # Validate new password
        if len(new_password) < 6:
            return False, "New password must be at least 6 characters long"
        
        # Update password
        self.users[email]["password"] = self._hash_password(new_password)
        self._save_users()
        
        return True, "Password changed successfully"
    
    def get_user_info(self, email: str) -> Dict[str, Any]:
        """Get user information"""
        user_info = self.users.get(email, {}).copy()
        # Remove password from user info
        user_info.pop("password", None)
        return user_info
    
    def save_user_history(self, email: str, history_entry: Dict[str, Any]):
        """Save user chat history"""
        history_data = self._load_history()
        
        if email not in history_data:
            history_data[email] = []
        
        history_data[email].append(history_entry)
        self._save_history(history_data)
    
    def get_user_history(self, email: str) -> List[Dict[str, Any]]:
        """Get user chat history"""
        history_data = self._load_history()
        return history_data.get(email, [])
    
    def save_user_feedback(self, email: str, feedback_entry: Dict[str, Any]):
        """Save user feedback"""
        feedback_data = self._load_feedback()
        
        if email not in feedback_data:
            feedback_data[email] = []
        
        # Check if feedback already exists for this response_id
        existing_feedback = feedback_data[email]
        response_id = feedback_entry.get("response_id")
        
        # Remove existing feedback for this response if it exists
        existing_feedback = [f for f in existing_feedback if f.get("response_id") != response_id]
        
        # Add new feedback
        existing_feedback.append(feedback_entry)
        feedback_data[email] = existing_feedback
        
        self._save_feedback(feedback_data)
    
    def get_user_feedback(self, email: str) -> List[Dict[str, Any]]:
        """Get user feedback"""
        feedback_data = self._load_feedback()
        return feedback_data.get(email, [])
    
    def delete_user(self, email: str) -> bool:
        """Delete a user and all their data"""
        if email not in self.users:
            return False
        
        # Remove user from users
        del self.users[email]
        self._save_users()
        
        # Remove user history
        history_data = self._load_history()
        if email in history_data:
            del history_data[email]
            self._save_history(history_data)
        
        # Remove user feedback
        feedback_data = self._load_feedback()
        if email in feedback_data:
            del feedback_data[email]
            self._save_feedback(feedback_data)
        
        return True
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users (for admin purposes)"""
        users_list = []
        for email, user_data in self.users.items():
            user_info = user_data.copy()
            user_info.pop("password", None)  # Remove password
            users_list.append(user_info)
        return users_list
    
    def get_user_stats(self, email: str) -> Dict[str, Any]:
        """Get user statistics"""
        if email not in self.users:
            return {}
        
        history = self.get_user_history(email)
        feedback = self.get_user_feedback(email)
        
        total_chats = len(history)
        total_feedback = len(feedback)
        positive_feedback = len([f for f in feedback if f.get("feedback") == "positive"])
        negative_feedback = len([f for f in feedback if f.get("feedback") == "negative"])
        
        satisfaction_rate = (positive_feedback / total_feedback * 100) if total_feedback > 0 else 0
        
        return {
            "total_chats": total_chats,
            "total_feedback": total_feedback,
            "positive_feedback": positive_feedback,
            "negative_feedback": negative_feedback,
            "satisfaction_rate": satisfaction_rate,
            "user_info": self.get_user_info(email)
        }
