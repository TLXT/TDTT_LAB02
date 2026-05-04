"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    APP_NAME: str = "To-Do App API"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = ""
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:8501",  # Streamlit default port
        "http://localhost:8000",
        "http://localhost:3000",
        "*"
    ]
    
    # Firebase
    FIREBASE_PROJECT_ID: str = "tdtt3-4112b"
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()