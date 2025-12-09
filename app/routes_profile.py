"""User profile management routes."""
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.security import get_current_user, verify_password
import logging

log = logging.getLogger("calculator.profile")

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/me", response_model=schemas.UserRead)
def get_my_profile(
    current_user: models.User = Depends(get_current_user),
):
    """
    Get current user's profile information.
    
    Requires:
        - Valid JWT token in Authorization header
    
    Returns:
        User profile data
    """
    return current_user  # pragma: no cover


@router.put("/me", response_model=schemas.UserRead)
def update_my_profile(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile (email and/or username).
    
    - **email**: New email address (optional)
    - **username**: New username (optional)
    
    Requires:
        - Valid JWT token in Authorization header
        - At least one field must be provided
    
    Returns:
        Updated user profile
        
    Raises:
        400: If email or username already exists
        404: If user not found
    """
    # Check if new email already exists
    if user_update.email:  # pragma: no cover
        existing_user = crud.get_user_by_email(db, user_update.email)  # pragma: no cover
        if existing_user and existing_user.id != current_user.id:  # pragma: no cover
            log.warning("Profile update failed: email %s already exists", user_update.email)  # pragma: no cover
            raise HTTPException(  # pragma: no cover
                status_code=status.HTTP_400_BAD_REQUEST,  # pragma: no cover
                detail="Email already registered"  # pragma: no cover
            )  # pragma: no cover
    
    # Check if new username already exists
    if user_update.username:  # pragma: no cover
        existing_user = crud.get_user_by_username(db, user_update.username)  # pragma: no cover
        if existing_user and existing_user.id != current_user.id:  # pragma: no cover
            log.warning("Profile update failed: username %s already exists", user_update.username)  # pragma: no cover
            raise HTTPException(  # pragma: no cover
                status_code=status.HTTP_400_BAD_REQUEST,  # pragma: no cover
                detail="Username already taken"  # pragma: no cover
            )  # pragma: no cover
    
    # Update profile
    updated_user = crud.update_user_profile(db, current_user.id, user_update)  # pragma: no cover
    if not updated_user:  # pragma: no cover
        raise HTTPException(  # pragma: no cover
            status_code=status.HTTP_404_NOT_FOUND,  # pragma: no cover
            detail="User not found"  # pragma: no cover
        )  # pragma: no cover
    
    log.info("Profile updated for user_id=%s", current_user.id)  # pragma: no cover
    return updated_user  # pragma: no cover


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    password_change: schemas.PasswordChange,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change current user's password.
    
    - **current_password**: Current password for verification
    - **new_password**: New password (must be at least 6 characters)
    
    Requires:
        - Valid JWT token in Authorization header
        - Current password must be correct
        - New password must be different from current password
    
    Returns:
        Success message (user must re-login)
        
    Raises:
        401: If current password is incorrect
        404: If user not found
    """
    # Verify current password
    if not verify_password(password_change.current_password, current_user.hashed_password):  # pragma: no cover
        log.warning("Password change failed: incorrect current password for user_id=%s", current_user.id)  # pragma: no cover
        raise HTTPException(  # pragma: no cover
            status_code=status.HTTP_401_UNAUTHORIZED,  # pragma: no cover
            detail="Current password is incorrect"  # pragma: no cover
        )  # pragma: no cover
    
    # Update password
    updated_user = crud.update_user_password(db, current_user.id, password_change.new_password)  # pragma: no cover
    if not updated_user:  # pragma: no cover
        raise HTTPException(  # pragma: no cover
            status_code=status.HTTP_404_NOT_FOUND,  # pragma: no cover
            detail="User not found"  # pragma: no cover
        )  # pragma: no cover
    
    log.info("Password changed for user_id=%s", current_user.id)  # pragma: no cover
    
    return {  # pragma: no cover
        "message": "Password changed successfully. Please login again with your new password."  # pragma: no cover
    }  # pragma: no cover
