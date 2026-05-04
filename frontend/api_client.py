"""
API Client for Backend Communication
Handles all HTTP requests to FastAPI backend
"""
import requests
from typing import Dict, List, Optional, Any
import streamlit as st


class APIClient:
    """Client for communicating with FastAPI backend"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def _get_headers(self, token: Optional[str] = None) -> Dict[str, str]:
        """Get headers with optional auth token"""
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers
    
    # Health check
    def health_check(self) -> Dict:
        """Check API health"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # Auth endpoints
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify Firebase token with backend"""
        try:
            response = self.session.get(
                f"{self.base_url}/auth/me",
                headers=self._get_headers(token)
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Token verification failed: {str(e)}")
            return None
    
    # Task endpoints
    def create_task(
        self, 
        token: str, 
        title: str, 
        description: str = "",
        status: str = "pending"
    ) -> Optional[Dict]:
        """Create a new task"""
        try:
            response = self.session.post(
                f"{self.base_url}/tasks/",
                headers=self._get_headers(token),
                json={
                    "title": title,
                    "description": description,
                    "status": status
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error creating task: {str(e)}")
            return None
    
    def get_tasks(self, token: str) -> Optional[Dict]:
        """Get all tasks for current user"""
        try:
            response = self.session.get(
                f"{self.base_url}/tasks/",
                headers=self._get_headers(token)
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching tasks: {str(e)}")
            return None
    
    def update_task(
        self, 
        token: str, 
        task_id: str, 
        update_data: Dict[str, Any]
    ) -> Optional[Dict]:
        """Update a task"""
        try:
            response = self.session.put(
                f"{self.base_url}/tasks/{task_id}",
                headers=self._get_headers(token),
                json=update_data
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error updating task: {str(e)}")
            return None
    
    def delete_task(self, token: str, task_id: str) -> bool:
        """Delete a task"""
        try:
            response = self.session.delete(
                f"{self.base_url}/tasks/{task_id}",
                headers=self._get_headers(token)
            )
            response.raise_for_status()
            return True
        except Exception as e:
            st.error(f"Error deleting task: {str(e)}")
            return False
    
    def get_statistics(self, token: str) -> Optional[Dict]:
        """Get task statistics"""
        try:
            response = self.session.get(
                f"{self.base_url}/tasks/statistics",
                headers=self._get_headers(token)
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching statistics: {str(e)}")
            return None


# Create singleton instance
api_client = APIClient()