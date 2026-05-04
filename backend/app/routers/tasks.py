"""
Tasks Router
Handles task CRUD operations
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from app.dependencies.auth import get_current_user
from app.schemas.tasks import (
    TaskCreate, 
    TaskUpdate, 
    TaskResponse, 
    TaskListResponse,
    MessageResponse
)
from app.services.firebase_service import firebase_service


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post(
    "/", 
    response_model=TaskResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task"
)
async def create_task(
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new task
    
    Args:
        task_data: Task creation data
        current_user: Current authenticated user
        
    Returns:
        TaskResponse: Created task
    """
    try:
        user_id = current_user['uid']
        
        task = await firebase_service.create_task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            status=task_data.status
        )
        
        return TaskResponse(**task)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )


@router.get(
    "/", 
    response_model=TaskListResponse,
    summary="Get all tasks for current user"
)
async def get_tasks(
    current_user: dict = Depends(get_current_user)
):
    """
    Get all tasks for the current authenticated user
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        TaskListResponse: List of tasks with total count
    """
    try:
        user_id = current_user['uid']
        
        tasks = await firebase_service.get_tasks(user_id)
        
        return TaskListResponse(
            tasks=[TaskResponse(**task) for task in tasks],
            total=len(tasks)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching tasks: {str(e)}"
        )


@router.get(
    "/statistics",
    summary="Get task statistics"
)
async def get_task_statistics(
    current_user: dict = Depends(get_current_user)
):
    """
    Get task statistics for the current user
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        dict: Statistics including total, pending, and completed counts
    """
    try:
        user_id = current_user['uid']
        stats = await firebase_service.get_task_statistics(user_id)
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching statistics: {str(e)}"
        )


@router.get(
    "/{task_id}", 
    response_model=TaskResponse,
    summary="Get a specific task"
)
async def get_task(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific task by ID
    
    Args:
        task_id: Task ID
        current_user: Current authenticated user
        
    Returns:
        TaskResponse: Task data
        
    Raises:
        HTTPException: If task not found or user is not authorized
    """
    user_id = current_user['uid']
    
    task = await firebase_service.get_task(task_id, user_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )
    
    return TaskResponse(**task)


@router.put(
    "/{task_id}", 
    response_model=TaskResponse,
    summary="Update a task"
)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update a task
    
    Args:
        task_id: Task ID
        task_update: Update data
        current_user: Current authenticated user
        
    Returns:
        TaskResponse: Updated task
        
    Raises:
        HTTPException: If task not found or user is not authorized
    """
    user_id = current_user['uid']
    
    # Only include non-None fields
    update_data = {k: v for k, v in task_update.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    try:
        task = await firebase_service.update_task(task_id, user_id, update_data)
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or you don't have permission to update it"
            )
        
        return TaskResponse(**task)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )


@router.delete(
    "/{task_id}", 
    response_model=MessageResponse,
    summary="Delete a task"
)
async def delete_task(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a task
    
    Args:
        task_id: Task ID
        current_user: Current authenticated user
        
    Returns:
        MessageResponse: Success message
        
    Raises:
        HTTPException: If task not found or user is not authorized
    """
    user_id = current_user['uid']
    
    success = await firebase_service.delete_task(task_id, user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to delete it"
        )
    
    return MessageResponse(message="Task deleted successfully")