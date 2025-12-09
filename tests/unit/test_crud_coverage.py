"""Additional unit tests for 100% CRUD coverage."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import crud, models, schemas
from app.security import hash_password


@pytest.fixture
def db():
    """Create test database."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestSessionLocal()
    yield session
    session.close()


class TestUpdateCalculationNotFound:
    """Test update_calculation with non-existent calculation."""
    
    def test_update_calculation_not_found(self, db):
        """Test updating non-existent calculation returns None."""
        calc_update = schemas.CalculationCreate(
            a=10.0,
            b=5.0,
            type="Add"
        )
        result = crud.update_calculation(db, calculation_id=999, calc_in=calc_update)
        assert result is None


class TestUpdateUserProfileNotFound:
    """Test update_user_profile with non-existent user."""
    
    def test_update_user_profile_not_found(self, db):
        """Test updating non-existent user profile returns None."""
        user_update = schemas.UserUpdate(email="new@example.com")
        result = crud.update_user_profile(db, user_id=999, user_update=user_update)
        assert result is None


class TestUpdateUserPasswordNotFound:
    """Test update_user_password with non-existent user."""
    
    def test_update_user_password_not_found(self, db):
        """Test updating non-existent user password returns None."""
        result = crud.update_user_password(db, user_id=999, new_password="newpass123")
        assert result is None


class TestGetUserCalculationStats:
    """Test get_user_calculation_stats edge cases."""
    
    def test_stats_no_calculations(self, db):
        """Test stats when user has no calculations."""
        # Create user
        user_data = schemas.UserCreate(
            email="test@example.com",
            username="testuser",
            password="testpass"
        )
        user = crud.create_user(db, user_data)
        
        # Get stats
        stats = crud.get_user_calculation_stats(db, user.id)
        
        assert stats["total_calculations"] == 0
        assert stats["operations_breakdown"] == {}
        assert stats["most_used_operation"] is None
        assert stats["average_result"] is None
    
    def test_stats_with_calculations(self, db):
        """Test stats with calculations."""
        # Create user
        user_data = schemas.UserCreate(
            email="test@example.com",
            username="testuser",
            password="testpass"
        )
        user = crud.create_user(db, user_data)
        
        # Create calculations
        calc1 = schemas.CalculationCreate(a=10.0, b=5.0, type="Add")
        calc2 = schemas.CalculationCreate(a=20.0, b=10.0, type="Add")
        calc3 = schemas.CalculationCreate(a=8.0, b=2.0, type="Multiply")
        
        crud.create_calculation(db, calc1, user.id)
        crud.create_calculation(db, calc2, user.id)
        crud.create_calculation(db, calc3, user.id)
        
        # Get stats
        stats = crud.get_user_calculation_stats(db, user.id)
        
        assert stats["total_calculations"] == 3
        assert stats["operations_breakdown"]["Add"] == 2
        assert stats["operations_breakdown"]["Multiply"] == 1
        assert stats["most_used_operation"] == "Add"
        assert stats["average_result"] == (15.0 + 30.0 + 16.0) / 3
    
    def test_stats_all_operation_types(self, db):
        """Test stats with all six operation types."""
        # Create user
        user_data = schemas.UserCreate(
            email="test@example.com",
            username="testuser",
            password="testpass"
        )
        user = crud.create_user(db, user_data)
        
        # Create one of each operation type
        calculations = [
            schemas.CalculationCreate(a=10.0, b=5.0, type="Add"),
            schemas.CalculationCreate(a=10.0, b=5.0, type="Sub"),
            schemas.CalculationCreate(a=10.0, b=5.0, type="Multiply"),
            schemas.CalculationCreate(a=10.0, b=5.0, type="Divide"),
            schemas.CalculationCreate(a=10.0, b=5.0, type="Power"),
            schemas.CalculationCreate(a=10.0, b=5.0, type="Modulus"),
        ]
        
        for calc in calculations:
            crud.create_calculation(db, calc, user.id)
        
        # Get stats
        stats = crud.get_user_calculation_stats(db, user.id)
        
        assert stats["total_calculations"] == 6
        assert len(stats["operations_breakdown"]) == 6
        assert all(count == 1 for count in stats["operations_breakdown"].values())


class TestDeleteCalculationNotFound:
    """Test delete_calculation with non-existent calculation."""
    
    def test_delete_calculation_not_found(self, db):
        """Test deleting non-existent calculation returns False."""
        result = crud.delete_calculation(db, calculation_id=999)
        assert result is False
    
    def test_delete_calculation_success(self, db):
        """Test successful deletion returns True."""
        # Create user
        user_data = schemas.UserCreate(
            email="test@example.com",
            username="testuser",
            password="testpass"
        )
        user = crud.create_user(db, user_data)
        
        # Create calculation
        calc_data = schemas.CalculationCreate(a=10.0, b=5.0, type="Add")
        calc = crud.create_calculation(db, calc_data, user.id)
        
        # Delete it
        result = crud.delete_calculation(db, calc.id)
        assert result is True
        
        # Verify it's gone
        assert crud.get_calculation(db, calc.id) is None
