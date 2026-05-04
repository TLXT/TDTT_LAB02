"""
Authentication Router
Handles authentication-related endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from firebase_admin import auth
from app.dependencies.auth import get_current_user
from pydantic import BaseModel, EmailStr
from typing import Optional


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


class UserInfoResponse(BaseModel):
    """User information response"""
    uid: str
    email: Optional[str] = None
    display_name: Optional[str] = None
    email_verified: bool = False


@router.get("/me", response_model=UserInfoResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information
    
    Returns:
        UserInfoResponse: Current user information
    """
    try:
        # Get full user information from Firebase
        user = auth.get_user(current_user['uid'])
        
        return UserInfoResponse(
            uid=user.uid,
            email=user.email,
            display_name=user.display_name,
            email_verified=user.email_verified
        )
    except auth.UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user info: {str(e)}"
        )


@router.post("/verify-token", response_model=UserInfoResponse)
async def verify_token(current_user: dict = Depends(get_current_user)):
    """
    Verify Firebase ID token
    
    Returns:
        UserInfoResponse: User information if token is valid
    """
    try:
        user = auth.get_user(current_user['uid'])
        
        return UserInfoResponse(
            uid=user.uid,
            email=user.email,
            display_name=user.display_name,
            email_verified=user.email_verified
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )