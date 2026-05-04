"""
Task Schemas
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    COMPLETED = "completed"


class TaskBase(BaseModel):
    """Base task schema"""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")


class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Task status")


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None


class TaskResponse(TaskBase):
    """Schema for task response"""
    id: str = Field(..., description="Task ID")
    user_id: str = Field(..., description="User ID who owns this task")
    status: TaskStatus = Field(..., description="Task status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "task_123",
                "user_id": "user_456",
                "title": "Complete lab assignment",
                "description": "Finish To-Do App with Firebase",
                "status": "pending",
                "created_at": "2026-05-04T10:30:00",
                "updated_at": "2026-05-04T10:30:00"
            }
        }


class TaskListResponse(BaseModel):
    """Schema for list of tasks response"""
    tasks: list[TaskResponse] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total number of tasks")

    class Config:
        json_schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": "task_123",
                        "user_id": "user_456",
                        "title": "Complete lab assignment",
                        "description": "Finish To-Do App with Firebase",
                        "status": "pending",
                        "created_at": "2026-05-04T10:30:00",
                        "updated_at": "2026-05-04T10:30:00"
                    }
                ],
                "total": 1
            }
        }


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str = Field(..., description="Response message")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Task deleted successfully"
            }
        }