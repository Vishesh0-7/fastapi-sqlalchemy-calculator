"""Calculation BREAD (Browse, Read, Edit, Add, Delete) routes."""
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, models
from app.database import get_db
from app.security import get_current_user

router = APIRouter(prefix="/calculations", tags=["calculations"])


@router.get("/", response_model=List[schemas.CalculationRead])
def browse_calculations(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Browse all calculations for the logged-in user (list with pagination).
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100)
    
    Requires:
        - Valid JWT token in Authorization header
    
    Returns:
        List of calculations owned by the current user
    """
    return crud.list_user_calculations(db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{calculation_id}", response_model=schemas.CalculationRead)
def read_calculation(
    calculation_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Read a specific calculation by ID.
    
    - **calculation_id**: ID of the calculation to retrieve
    
    Requires:
        - Valid JWT token in Authorization header
        - Calculation must belong to the current user
    
    Raises:
        404: If calculation not found or doesn't belong to user
    """
    calculation = crud.get_calculation(db, calculation_id)
    if calculation is None or calculation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    return calculation


@router.post("/", response_model=schemas.CalculationRead, status_code=status.HTTP_201_CREATED)
def add_calculation(
    calculation: schemas.CalculationCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a new calculation.
    
    - **a**: First number
    - **b**: Second number
    - **type**: Operation type (Add, Sub, Multiply, Divide)
    
    Requires:
        - Valid JWT token in Authorization header
    
    Automatically associates calculation with the logged-in user.
    
    Raises:
        400: If validation fails (e.g., division by zero)
        401: If not authenticated
        422: If invalid operation type
    """
    try:
        return crud.create_calculation(db, calculation, current_user.id)
    except ValueError as e:  # pragma: no cover
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))  # pragma: no cover
    except ZeroDivisionError as e:  # pragma: no cover
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))  # pragma: no cover


@router.put("/{calculation_id}", response_model=schemas.CalculationRead)
def edit_calculation(
    calculation_id: int,
    calculation: schemas.CalculationCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Edit an existing calculation.
    
    Updates the calculation values and recomputes the result.
    
    - **calculation_id**: ID of the calculation to update
    - **a**: New first number
    - **b**: New second number
    - **type**: New operation type
    
    Requires:
        - Valid JWT token in Authorization header
        - Calculation must belong to the current user
    
    Raises:
        404: If calculation not found or doesn't belong to user
        401: If not authenticated
        400: If validation fails (e.g., division by zero)
    """
    # Check if calculation exists and belongs to user
    existing_calc = crud.get_calculation(db, calculation_id)
    if existing_calc is None or existing_calc.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    try:
        updated_calc = crud.update_calculation(db, calculation_id, calculation)
        return updated_calc
    except ValueError as e:  # pragma: no cover
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ZeroDivisionError as e:  # pragma: no cover
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{calculation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(
    calculation_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a calculation by ID.
    
    - **calculation_id**: ID of the calculation to delete
    
    Requires:
        - Valid JWT token in Authorization header
        - Calculation must belong to the current user
    
    Raises:
        404: If calculation not found or doesn't belong to user
        401: If not authenticated
    """
    # Check if calculation exists and belongs to user
    existing_calc = crud.get_calculation(db, calculation_id)
    if existing_calc is None or existing_calc.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    crud.delete_calculation(db, calculation_id)
    return None
