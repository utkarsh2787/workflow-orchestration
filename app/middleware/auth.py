from fastapi import Request, HTTPException, status, Depends, Cookie
from typing import Optional
from sqlalchemy.orm import Session

from app.services.auth import verify_token
from app.models.user import get_user_by_email
from app.db.session import get_db


def get_current_user_from_cookie(
    access_token: Optional[str] = Cookie(None),
    session: Session = Depends(get_db)
):
    """Get current user from JWT token in cookie"""
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    try:
        user_id = verify_token(access_token)
        # You could also get user from database here if needed
        return {"user_id": int(user_id)}
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )


def get_current_user_optional(
    access_token: Optional[str] = Cookie(None),
    session: Session = Depends(get_db)
):
    """Get current user from JWT token in cookie (optional - doesn't raise error if not authenticated)"""
    if not access_token:
        return None
    
    try:
        user_id = verify_token(access_token)
        return {"user_id": int(user_id)}
    except HTTPException:
        return None
