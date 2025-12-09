"""Dashboard and statistics routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.security import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=schemas.CalculationStats)
def get_my_statistics(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get calculation statistics for the current user.
    
    Returns:
        - **total_calculations**: Total number of calculations
        - **operations_breakdown**: Count of each operation type
        - **most_used_operation**: Most frequently used operation
        - **average_result**: Average result of all calculations
    
    Requires:
        - Valid JWT token in Authorization header
    """
    stats = crud.get_user_calculation_stats(db, current_user.id)  # pragma: no cover
    return schemas.CalculationStats(**stats)  # pragma: no cover
