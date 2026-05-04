"""
Firebase Service
Handles all Firestore database operations for tasks
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from app.core.firebase_config import firebase_config
from app.schemas.tasks import TaskStatus

class FirebaseService:
    """Service class for Firebase Firestore operations"""
    
    def __init__(self):
        self.db = firebase_config.get_firestore_client()
        self.collection_name = 'tasks'
        
    async def create_task(
        self, 
        user_id: str, 
        title: str, 
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.PENDING
    ) -> Dict[str, Any]:
        """
        Create a new task in Firestore
        """
        # Create a new document reference
        task_ref = self.db.collection(self.collection_name).document()
        task_id = task_ref.id
        
        # Prepare task data
        now = datetime.utcnow()
        task_data = {
            'id': task_id,
            'user_id': user_id,
            'title': title,
            'description': description or '',
            'status': status.value if isinstance(status, TaskStatus) else status,
            'created_at': now,
            'updated_at': now
        }
        
        # Save to Firestore
        task_ref.set(task_data)
        
        return task_data

    async def get_tasks(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all tasks for a specific user
        """
        tasks_ref = self.db.collection(self.collection_name)
        
        # BỎ order_by ở đây để né lỗi Composite Index của Firebase
        query = tasks_ref.where(filter=FieldFilter('user_id', '==', user_id))
        
        tasks = []
        for doc in query.stream():
            task_data = doc.to_dict()
            
            # VÁ LỖI DỮ LIỆU RÁC: Đảm bảo không bị lỗi 500 từ Pydantic
            if 'id' not in task_data: task_data['id'] = doc.id
            if 'user_id' not in task_data: task_data['user_id'] = user_id
            if 'title' not in task_data: task_data['title'] = "Không có tiêu đề"
            if 'status' not in task_data: task_data['status'] = TaskStatus.PENDING.value
            if 'created_at' not in task_data: task_data['created_at'] = datetime.utcnow()
            if 'updated_at' not in task_data: task_data['updated_at'] = task_data['created_at']
            if 'description' not in task_data: task_data['description'] = ""

            tasks.append(task_data)
            
        # SẮP XẾP BẰNG PYTHON (Mới nhất lên đầu)
        try:
            tasks.sort(key=lambda x: x.get('created_at'), reverse=True)
        except TypeError:
            # Bỏ qua lỗi sắp xếp nếu kiểu thời gian bị lẫn lộn giữa các document cũ
            pass
            
        return tasks

    async def get_task(self, task_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific task by ID
        """
        task_ref = self.db.collection(self.collection_name).document(task_id)
        task_doc = task_ref.get()
        
        if not task_doc.exists:
            return None
            
        task_data = task_doc.to_dict()
        
        # Check if user owns this task
        if task_data.get('user_id') != user_id:
            return None
            
        return task_data

    async def update_task(
        self, 
        task_id: str, 
        user_id: str, 
        update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Update a task
        """
        task_ref = self.db.collection(self.collection_name).document(task_id)
        task_doc = task_ref.get()
        
        if not task_doc.exists:
            return None
            
        task_data = task_doc.to_dict()
        
        # Check if user owns this task
        if task_data.get('user_id') != user_id:
            return None
            
        # Prepare update data
        update_fields = {}
        for key, value in update_data.items():
            if value is not None:
                if isinstance(value, TaskStatus):
                    update_fields[key] = value.value
                else:
                    update_fields[key] = value
                    
        # Always update the updated_at timestamp
        update_fields['updated_at'] = datetime.utcnow()
        
        # Update in Firestore
        task_ref.update(update_fields)
        
        # Get and return updated task
        updated_doc = task_ref.get()
        return updated_doc.to_dict()

    async def delete_task(self, task_id: str, user_id: str) -> bool:
        """
        Delete a task
        """
        task_ref = self.db.collection(self.collection_name).document(task_id)
        task_doc = task_ref.get()
        
        if not task_doc.exists:
            return False
            
        task_data = task_doc.to_dict()
        
        # Check if user owns this task
        if task_data.get('user_id') != user_id:
            return False
            
        # Delete from Firestore
        task_ref.delete()
        
        return True

    async def get_task_statistics(self, user_id: str) -> Dict[str, int]:
        """
        Get task statistics for a user
        """
        tasks = await self.get_tasks(user_id)
        
        total = len(tasks)
        pending = sum(1 for task in tasks if task.get('status') == TaskStatus.PENDING.value)
        completed = sum(1 for task in tasks if task.get('status') == TaskStatus.COMPLETED.value)
        
        return {
            'total': total,
            'pending': pending,
            'completed': completed
        }

# Create singleton instance
firebase_service = FirebaseService()