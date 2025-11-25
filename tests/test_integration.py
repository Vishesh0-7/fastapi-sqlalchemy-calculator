"""Integration tests for calculation CRUD operations with database."""
import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import ValidationError
from app.database import Base
from app.models import User, Calculation
from app.schemas import CalculationCreate, UserCreate
from app import crud


# Test database setup - use PostgreSQL if DATABASE_URL is set, otherwise SQLite
TEST_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test_integration.db")

@pytest.fixture(scope="function")
def test_db():
    """Create a fresh test database for each test."""
    connect_args = {"check_same_thread": False} if "sqlite" in TEST_DATABASE_URL else {}
    engine = create_engine(TEST_DATABASE_URL, connect_args=connect_args)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(test_db):
    """Create a test user for calculations."""
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        password="testpass123"
    )
    user = crud.create_user(test_db, user_data)
    return user


class TestCalculationCRUD:
    """Test suite for Calculation CRUD operations."""
    
    def test_create_calculation_with_user(self, test_db, test_user):
        """Test inserting a calculation with user_id."""
        calc_in = CalculationCreate(a=10, b=5, type="Add")
        calc = crud.create_calculation(test_db, calc_in, user_id=test_user.id)
        
        assert calc.id is not None
        assert calc.a == 10
        assert calc.b == 5
        assert calc.type == "Add"
        assert calc.result == 15
        assert calc.user_id == test_user.id
    
    def test_create_calculation_without_user(self, test_db):
        """Test inserting a calculation without user_id."""
        calc_in = CalculationCreate(a=8, b=3, type="Sub")
        calc = crud.create_calculation(test_db, calc_in, user_id=None)
        
        assert calc.id is not None
        assert calc.a == 8
        assert calc.b == 3
        assert calc.type == "Sub"
        assert calc.result == 5
        assert calc.user_id is None
    
    def test_calculation_result_add(self, test_db):
        """Test Add operation result is computed correctly."""
        calc_in = CalculationCreate(a=7, b=3, type="Add")
        calc = crud.create_calculation(test_db, calc_in)
        
        assert calc.result == 10
    
    def test_calculation_result_sub(self, test_db):
        """Test Sub operation result is computed correctly."""
        calc_in = CalculationCreate(a=15, b=7, type="Sub")
        calc = crud.create_calculation(test_db, calc_in)
        
        assert calc.result == 8
    
    def test_calculation_result_multiply(self, test_db):
        """Test Multiply operation result is computed correctly."""
        calc_in = CalculationCreate(a=6, b=7, type="Multiply")
        calc = crud.create_calculation(test_db, calc_in)
        
        assert calc.result == 42
    
    def test_calculation_result_divide(self, test_db):
        """Test Divide operation result is computed correctly."""
        calc_in = CalculationCreate(a=20, b=4, type="Divide")
        calc = crud.create_calculation(test_db, calc_in)
        
        assert calc.result == 5.0
    
    def test_invalid_type_rejected(self, test_db):
        """Test invalid operation type is rejected by schema validation."""
        with pytest.raises(ValidationError):
            CalculationCreate(a=5, b=3, type="Power")
    
    def test_division_by_zero_rejected(self, test_db):
        """Test division by zero is rejected by schema validation."""
        with pytest.raises(ValidationError) as exc_info:
            CalculationCreate(a=10, b=0, type="Divide")
        
        errors = exc_info.value.errors()
        assert any("Division by zero" in str(err) for err in errors)
    
    def test_get_calculation(self, test_db):
        """Test retrieving a calculation by ID."""
        calc_in = CalculationCreate(a=12, b=4, type="Multiply")
        created_calc = crud.create_calculation(test_db, calc_in)
        
        retrieved_calc = crud.get_calculation(test_db, created_calc.id)
        
        assert retrieved_calc is not None
        assert retrieved_calc.id == created_calc.id
        assert retrieved_calc.a == 12
        assert retrieved_calc.b == 4
        assert retrieved_calc.type == "Multiply"
        assert retrieved_calc.result == 48
    
    def test_get_nonexistent_calculation(self, test_db):
        """Test retrieving a calculation that doesn't exist returns None."""
        calc = crud.get_calculation(test_db, 99999)
        assert calc is None
    
    def test_list_calculations(self, test_db):
        """Test listing all calculations."""
        # Create multiple calculations
        calc1_in = CalculationCreate(a=5, b=3, type="Add")
        calc2_in = CalculationCreate(a=10, b=2, type="Divide")
        calc3_in = CalculationCreate(a=7, b=4, type="Multiply")
        
        crud.create_calculation(test_db, calc1_in)
        crud.create_calculation(test_db, calc2_in)
        crud.create_calculation(test_db, calc3_in)
        
        calculations = crud.list_calculations(test_db)
        
        assert len(calculations) == 3
        assert calculations[0].result == 8
        assert calculations[1].result == 5.0
        assert calculations[2].result == 28
    
    def test_list_user_calculations(self, test_db, test_user):
        """Test listing calculations for a specific user."""
        # Create calculations for user
        calc1_in = CalculationCreate(a=5, b=3, type="Add")
        calc2_in = CalculationCreate(a=10, b=2, type="Sub")
        
        crud.create_calculation(test_db, calc1_in, user_id=test_user.id)
        crud.create_calculation(test_db, calc2_in, user_id=test_user.id)
        
        # Create calculation without user
        calc3_in = CalculationCreate(a=7, b=4, type="Multiply")
        crud.create_calculation(test_db, calc3_in, user_id=None)
        
        user_calculations = crud.list_user_calculations(test_db, test_user.id)
        
        assert len(user_calculations) == 2
        assert all(calc.user_id == test_user.id for calc in user_calculations)
    
    def test_calculation_float_precision(self, test_db):
        """Test calculations with float values maintain precision."""
        calc_in = CalculationCreate(a=0.1, b=0.2, type="Add")
        calc = crud.create_calculation(test_db, calc_in)
        
        # Allow for floating point precision
        assert pytest.approx(calc.result, rel=1e-9) == 0.3
    
    def test_calculation_with_negative_numbers(self, test_db):
        """Test calculations with negative numbers."""
        calc_in = CalculationCreate(a=-10, b=5, type="Add")
        calc = crud.create_calculation(test_db, calc_in)
        
        assert calc.result == -5
    
    def test_relationship_user_to_calculations(self, test_db, test_user):
        """Test SQLAlchemy relationship from User to Calculations."""
        calc1_in = CalculationCreate(a=5, b=3, type="Add")
        calc2_in = CalculationCreate(a=10, b=2, type="Multiply")
        
        crud.create_calculation(test_db, calc1_in, user_id=test_user.id)
        crud.create_calculation(test_db, calc2_in, user_id=test_user.id)
        
        # Refresh user to get updated relationships
        test_db.refresh(test_user)
        
        assert len(test_user.calculations) == 2
        assert test_user.calculations[0].type in ["Add", "Multiply"]
        assert test_user.calculations[1].type in ["Add", "Multiply"]
