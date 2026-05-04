"""
Firebase Configuration Module
Handles Firebase Admin SDK initialization
"""
import firebase_admin
from firebase_admin import credentials, firestore, auth
import json
import os
from typing import Optional


class FirebaseConfig:
    """Singleton class for Firebase configuration"""
    
    _instance: Optional['FirebaseConfig'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseConfig, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialize_firebase()
            FirebaseConfig._initialized = True
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK using secrets.toml"""
        try:
            # Check if Firebase is already initialized
            firebase_admin.get_app()
            print("Firebase already initialized")
        except ValueError:
            # Initialize Firebase for the first time
            print("Initializing Firebase...")
            
            # 1. Định vị đường dẫn tới file secrets.toml
            # Giả sử secrets.toml nằm ở thư mục root của dự án (hoặc thư mục .streamlit)
            # Bạn cần điều chỉnh số lượng '..' cho đúng với cấu trúc thực tế
            # Lùi 3 cấp ra thư mục PROJECT, sau đó đi vào .streamlit
            secrets_path = os.path.join(
                os.path.dirname(__file__), 
                '..', '..', '..', 
                '.streamlit', 
                'secrets.toml'
            )
            
            if os.path.exists(secrets_path):
                # 2. Đọc file secrets.toml
                try:
                    import tomllib # Python 3.11+
                    with open(secrets_path, "rb") as f:
                        secrets = tomllib.load(f)
                except ImportError:
                    import toml # Python 3.10 trở xuống
                    with open(secrets_path, "r", encoding="utf-8") as f:
                        secrets = toml.load(f)
                
                # 3. Trích xuất phần [firebase_admin] và đưa vào Certificate
                if "firebase_admin" in secrets:
                    firebase_admin_dict = secrets["firebase_admin"]
                    
                    # Firebase yêu cầu khóa private_key phải có các ký tự xuống dòng thực sự
                    # TOML đôi khi đọc chuỗi "\n" thành ký tự literal, ta cần replace nó lại
                    if "\\n" in firebase_admin_dict.get("private_key", ""):
                        firebase_admin_dict["private_key"] = firebase_admin_dict["private_key"].replace("\\n", "\n")
                    
                    try:
                        cred = credentials.Certificate(firebase_admin_dict)
                        firebase_admin.initialize_app(cred)
                        print("Firebase initialized successfully with secrets.toml")
                    except Exception as e:
                        print(f"Warning: Could not initialize Firebase app: {e}")
                else:
                    print("Warning: [firebase_admin] section not found in secrets.toml")
            else:
                print(f"Warning: secrets.toml not found at {secrets_path}")
            
            # Initialize Firestore client
            try:
                self.db = firestore.client()
                print("Firestore client initialized successfully")
            except Exception as e:
                print(f"Warning: Could not initialize Firestore: {e}")
                self.db = None
    
    def get_firestore_client(self):
        """Get Firestore database client"""
        return self.db
    
    def get_auth(self):
        """Get Firebase Auth instance"""
        return auth


# Create singleton instance
firebase_config = FirebaseConfig()