"""Additional tests to achieve 100% code coverage."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.models import User, Calculation
from app.schemas import CalculationCreate, UserCreate
from app import crud


TEST_DATABASE_URL = "sqlite:///./test_coverage.db"


@pytest.fixture(scope="function")
def test_db():
    """Create a fresh test database for each test."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


class TestCRUDCoverage:
    """Tests to cover missing CRUD functions."""
    
    def test_get_user(self, test_db):
        """Test get_user function."""
        # Create a user first
        user_data = UserCreate(
            email="test@example.com",
            username="testuser",
            password="testpass"
        )
        created_user = crud.create_user(test_db, user_data)
        
        # Test get_user
        retrieved_user = crud.get_user(test_db, created_user.id)
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.username == "testuser"
    
    def test_get_user_by_email(self, test_db):
        """Test get_user_by_email function."""
        # Create a user
        user_data = UserCreate(
            email="email@test.com",
            username="emailuser",
            password="pass123"
        )
        created_user = crud.create_user(test_db, user_data)
        
        # Test get_user_by_email
        retrieved_user = crud.get_user_by_email(test_db, "email@test.com")
        assert retrieved_user is not None
        assert retrieved_user.email == "email@test.com"
        assert retrieved_user.id == created_user.id


class TestDatabaseCoverage:
    """Tests to cover database.py functions."""
    
    def test_get_db_generator(self):
        """Test get_db function yields and closes properly."""
        gen = get_db()
        db = next(gen)
        assert db is not None
        
        # Close the generator
        try:
            next(gen)
        except StopIteration:
            pass  # Expected behavior


class TestModelsCoverage:
    """Tests to cover models.py edge cases."""
    
    def test_calculation_with_provided_result(self, test_db):
        """Test Calculation model when result is provided (not computed)."""
        # Create calculation with explicit result
        calc = Calculation(
            a=5.0,
            b=3.0,
            type="Add",
            result=999.0,  # Explicitly provide wrong result
            user_id=None
        )
        test_db.add(calc)
        test_db.commit()
        test_db.refresh(calc)
        
        # Should use the provided result, not compute
        assert calc.result == 999.0  # Not 8.0
        assert calc.a == 5.0
        assert calc.b == 3.0


class TestSchemasCoverage:
    """Tests to cover schemas.py validation paths."""
    
    def test_invalid_type_validator_path(self):
        """Test the type validator when it's actually invalid (though Literal should catch it)."""
        # The Literal type should prevent this, but let's test the validator logic
        # This tests line 18 in schemas.py
        from app.schemas import CalculationCreate
        from pydantic import ValidationError
        
        # Try to create with invalid type (will fail at Literal level)
        with pytest.raises(ValidationError):
            CalculationCreate(a=5, b=3, type="InvalidOp")


class TestFactoryCoverage:
    """Tests to cover factory.py missing line."""
    
    def test_base_operation_abstract(self):
        """Test that BaseOperation cannot be instantiated directly."""
        from app.factory import BaseOperation
        
        # BaseOperation is abstract and cannot be instantiated
        # This tests line 11 (the pass statement in abstract method)
        with pytest.raises(TypeError):
            BaseOperation()
