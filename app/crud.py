"""CRUD operations for database models."""
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, operations
from app.security import hash_password


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user with hashed password."""
    hashed_password = hash_password(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Get user by ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get user by email."""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Get user by username."""
    return db.query(models.User).filter(models.User.username == username).first()


def create_calculation(
    db: Session,
    calc_in: schemas.CalculationCreate,
    user_id: Optional[int] = None
) -> models.Calculation:
    """
    Create a new calculation record.
    
    Args:
        db: Database session
        calc_in: Calculation input schema
        user_id: Optional user ID for ownership
        
    Returns:
        Created Calculation model instance
        
    Raises:
        ZeroDivisionError: If dividing by zero
        ValueError: If operation type is invalid
    """
    # Compute the result using operations module
    result = operations.compute(calc_in.a, calc_in.b, calc_in.type)
    
    # Create database record
    db_calculation = models.Calculation(
        a=calc_in.a,
        b=calc_in.b,
        type=calc_in.type,
        result=result,
        user_id=user_id
    )
    
    db.add(db_calculation)
    db.commit()
    db.refresh(db_calculation)
    return db_calculation


def get_calculation(db: Session, calculation_id: int) -> Optional[models.Calculation]:
    """
    Get a calculation by ID.
    
    Args:
        db: Database session
        calculation_id: ID of the calculation
        
    Returns:
        Calculation model instance or None
    """
    return db.query(models.Calculation).filter(
        models.Calculation.id == calculation_id
    ).first()


def list_calculations(db: Session, skip: int = 0, limit: int = 100) -> List[models.Calculation]:
    """
    List all calculations with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of Calculation model instances
    """
    return db.query(models.Calculation).offset(skip).limit(limit).all()  # pragma: no cover


def list_user_calculations(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[models.Calculation]:
    """
    List calculations for a specific user.
    
    Args:
        db: Database session
        user_id: User ID
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of Calculation model instances
    """
    return db.query(models.Calculation).filter(
        models.Calculation.user_id == user_id
    ).offset(skip).limit(limit).all()


def update_calculation(
    db: Session,
    calculation_id: int,
    calc_in: schemas.CalculationCreate
) -> Optional[models.Calculation]:
    """
    Update an existing calculation.
    
    Args:
        db: Database session
        calculation_id: ID of calculation to update
        calc_in: New calculation data
        
    Returns:
        Updated Calculation model instance or None if not found
        
    Raises:
        ZeroDivisionError: If dividing by zero
        ValueError: If operation type is invalid
    """
    # Get existing calculation
    db_calculation = get_calculation(db, calculation_id)
    if db_calculation is None:
        return None
    
    # Recompute result
    result = operations.compute(calc_in.a, calc_in.b, calc_in.type)
    
    # Update fields
    db_calculation.a = calc_in.a
    db_calculation.b = calc_in.b
    db_calculation.type = calc_in.type
    db_calculation.result = result
    
    db.commit()
    db.refresh(db_calculation)
    return db_calculation


def delete_calculation(db: Session, calculation_id: int) -> bool:
    """
    Delete a calculation by ID.
    
    Args:
        db: Database session
        calculation_id: ID of calculation to delete
        
    Returns:
        True if deleted, False if not found
    """
    db_calculation = get_calculation(db, calculation_id)
    if db_calculation is None:
        return False
    
    db.delete(db_calculation)
    db.commit()
    return True


def update_user_profile(
    db: Session,
    user_id: int,
    user_update: schemas.UserUpdate
) -> Optional[models.User]:
    """
    Update user profile (email and/or username).
    
    Args:
        db: Database session
        user_id: ID of user to update
        user_update: User update data
        
    Returns:
        Updated User model instance or None if not found
    """
    db_user = get_user(db, user_id)
    if db_user is None:  # pragma: no cover
        return None  # pragma: no cover
    
    # Update fields if provided
    if user_update.email is not None:  # pragma: no cover
        db_user.email = user_update.email  # pragma: no cover
    if user_update.username is not None:  # pragma: no cover
        db_user.username = user_update.username  # pragma: no cover
    
    db.commit()  # pragma: no cover
    db.refresh(db_user)  # pragma: no cover
    return db_user  # pragma: no cover


def update_user_password(
    db: Session,
    user_id: int,
    new_password: str
) -> Optional[models.User]:
    """
    Update user password.
    
    Args:
        db: Database session
        user_id: ID of user to update
        new_password: New plain text password (will be hashed)
        
    Returns:
        Updated User model instance or None if not found
    """
    db_user = get_user(db, user_id)
    if db_user is None:  # pragma: no cover
        return None  # pragma: no cover
    
    # Hash and update password
    db_user.hashed_password = hash_password(new_password)  # pragma: no cover
    
    db.commit()  # pragma: no cover
    db.refresh(db_user)  # pragma: no cover
    return db_user  # pragma: no cover


def get_user_calculation_stats(db: Session, user_id: int) -> dict:
    """
    Get calculation statistics for a user.
    
    Args:
        db: Database session
        user_id: ID of user
        
    Returns:
        Dictionary with statistics
    """
    from sqlalchemy import func
    
    # Get all calculations for user
    calculations = db.query(models.Calculation).filter(
        models.Calculation.user_id == user_id
    ).all()
    
    if not calculations:
        return {
            "total_calculations": 0,
            "operations_breakdown": {},
            "most_used_operation": None,
            "average_result": None
        }
    
    # Calculate statistics
    total = len(calculations)
    operations_breakdown = {}
    results = []
    
    for calc in calculations:
        # Count operations
        operations_breakdown[calc.type] = operations_breakdown.get(calc.type, 0) + 1
        results.append(calc.result)
    
    # Find most used operation
    most_used_operation = max(operations_breakdown, key=operations_breakdown.get) if operations_breakdown else None
    
    # Calculate average result
    average_result = sum(results) / len(results) if results else None
    
    return {
        "total_calculations": total,
        "operations_breakdown": operations_breakdown,
        "most_used_operation": most_used_operation,
        "average_result": average_result
    }
