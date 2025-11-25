"""Final tests to achieve 100% code coverage."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, mock_open
from app.main import app
from app.database import Base, get_db
from app import crud, schemas
from app.factory import BaseOperation
from app.models import Calculation


TEST_DATABASE_URL = "sqlite:///./test_100.db"


@pytest.fixture(scope="function")
def test_db_session():
    """Create a test database session."""
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


@pytest.fixture
def client(test_db_session):
    """Create a test client with overridden database."""
    def override_get_db():
        try:
            yield test_db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


class TestMissingLines:
    """Tests to cover all remaining missing lines."""
    
    def test_database_url_replacement(self):
        """Test database.py line 15 - postgres:// to postgresql:// replacement."""
        import os
        from unittest.mock import patch
        
        # Test when DATABASE_URL starts with postgres://
        with patch.dict(os.environ, {"DATABASE_URL": "postgres://user:pass@localhost/db"}):
            # Re-import to trigger the URL replacement logic
            import importlib
            from app import database
            importlib.reload(database)
            assert database.DATABASE_URL == "postgresql://user:pass@localhost/db"
    
    def test_schema_invalid_type_error(self):
        """Test schemas.py line 18 - ValueError in type validator."""
        # Pydantic V2 validates Literal at a higher level, so the custom validator
        # is not reached. The line 18 in schemas.py is unreachable with Pydantic V2.
        # Let's test that invalid types are rejected by Pydantic
        from pydantic import ValidationError
        with pytest.raises(ValidationError) as exc_info:
            schemas.CalculationCreate(a=1, b=2, type="InvalidType")
        assert "Input should be" in str(exc_info.value)
    
    def test_model_with_explicit_result(self, test_db_session):
        """Test models.py lines 44-46 - else branch with explicit result."""
        calc = Calculation(a=5, b=3, type="Add", result=999)
        test_db_session.add(calc)
        test_db_session.commit()
        test_db_session.refresh(calc)
        # When result is provided explicitly, it should use that value
        assert calc.result == 999
    
    def test_base_operation_cannot_instantiate(self):
        """Test factory.py line 11 - abstract method in BaseOperation."""
        with pytest.raises(TypeError) as exc_info:
            BaseOperation()
        assert "abstract" in str(exc_info.value).lower()
    
    def test_middleware_exception_handling(self, client, monkeypatch):
        """Test main.py lines 41-43 - exception handling in middleware."""
        # Mock the call_next to raise an exception
        async def mock_call_next(request):
            raise Exception("Test exception")
        
        # Create a custom route that will trigger the exception
        from fastapi import Request
        from fastapi.responses import JSONResponse
        
        @app.get("/test-error")
        async def test_error_route():
            raise Exception("Test error")
        
        # Call the endpoint
        response = client.get("/test-error")
        # Should return 500 due to exception
        assert response.status_code == 500
    
    def test_startup_event_coverage(self):
        """Test main.py lines 25-26 - startup event."""
        # The startup event is already triggered when the app starts
        # but we can test it explicitly
        from app.main import startup_event
        startup_event()
        # If no exception, the tables were created successfully
        assert True
    
    def test_create_calculation_value_error(self, client, test_db_session):
        """Test main.py lines 103-104 - ValueError exception handling."""
        # Try to create a calculation with invalid data that raises ValueError
        # This might happen if factory raises ValueError
        with patch('app.crud.create_calculation') as mock_create:
            mock_create.side_effect = ValueError("Test value error")
            response = client.post(
                "/calculations/",
                json={"a": 10, "b": 5, "type": "Add"}
            )
            assert response.status_code == 400
            assert "Test value error" in response.json()["detail"]
    
    def test_create_calculation_zero_division_error(self, client, test_db_session):
        """Test main.py lines 105-106 - ZeroDivisionError exception handling."""
        # This is caught by Pydantic validation before reaching CRUD
        # But we can test the exception handler by mocking
        with patch('app.crud.create_calculation') as mock_create:
            mock_create.side_effect = ZeroDivisionError("Division by zero")
            response = client.post(
                "/calculations/",
                json={"a": 10, "b": 5, "type": "Add"}
            )
            assert response.status_code == 400
            assert "Division by zero" in response.json()["detail"]


class TestDatabaseURLHandling:
    """Test DATABASE_URL handling in database.py."""
    
    def test_database_url_no_replacement_needed(self):
        """Test when DATABASE_URL doesn't need replacement."""
        import os
        from unittest.mock import patch
        
        # Test when DATABASE_URL starts with something else
        with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///./test.db"}):
            import importlib
            from app import database
            importlib.reload(database)
            # Should remain unchanged
            assert database.DATABASE_URL == "sqlite:///./test.db"


class TestFullIntegrationFlow:
    """Integration tests for complete flows."""
    
    def test_complete_user_calculation_flow(self, client, test_db_session):
        """Test complete flow: create user, create calculations, list them."""
        # Create a user
        user_data = {
            "email": "complete@test.com",
            "username": "completeuser",
            "password": "password123"
        }
        user = crud.create_user(test_db_session, schemas.UserCreate(**user_data))
        
        # Create multiple calculations for this user
        calcs = [
            {"a": 10, "b": 5, "type": "Add"},
            {"a": 20, "b": 4, "type": "Divide"},
            {"a": 7, "b": 8, "type": "Multiply"},
        ]
        
        for calc in calcs:
            response = client.post(
                f"/calculations/?user_id={user.id}",
                json=calc
            )
            assert response.status_code == 201
        
        # List all calculations for the user
        response = client.get(f"/users/{user.id}/calculations/")
        assert response.status_code == 200
        user_calcs = response.json()
        assert len(user_calcs) >= 3
        
        # Verify each calculation
        for calc_data in user_calcs:
            assert calc_data["user_id"] == user.id
            assert "result" in calc_data


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_calculation_with_floats(self, client):
        """Test calculations with floating point numbers."""
        response = client.post(
            "/calculations/",
            json={"a": 10.5, "b": 2.5, "type": "Add"}
        )
        assert response.status_code == 201
        assert response.json()["result"] == 13.0
    
    def test_calculation_with_negative_numbers(self, client):
        """Test calculations with negative numbers."""
        response = client.post(
            "/calculations/",
            json={"a": -10, "b": 5, "type": "Add"}
        )
        assert response.status_code == 201
        assert response.json()["result"] == -5
    
    def test_large_pagination(self, client):
        """Test pagination with large skip value."""
        response = client.get("/calculations/?skip=1000&limit=10")
        assert response.status_code == 200
        # Should return empty list if no calculations
        assert isinstance(response.json(), list)


class TestAllOperationEndpoints:
    """Comprehensive tests for all legacy operation endpoints."""
    
    def test_all_add_endpoint(self, client):
        """Test /add endpoint thoroughly."""
        response = client.get("/add?a=100&b=200")
        assert response.status_code == 200
        assert response.json()["result"] == 300
    
    def test_all_sub_endpoint(self, client):
        """Test /sub endpoint thoroughly."""
        response = client.get("/sub?a=50&b=30")
        assert response.status_code == 200
        assert response.json()["result"] == 20
    
    def test_all_mul_endpoint(self, client):
        """Test /mul endpoint thoroughly."""
        response = client.get("/mul?a=12&b=12")
        assert response.status_code == 200
        assert response.json()["result"] == 144
    
    def test_all_div_endpoint_multiple(self, client):
        """Test /div endpoint with various inputs."""
        # Valid division
        response = client.get("/div?a=100&b=5")
        assert response.status_code == 200
        assert response.json()["result"] == 20
        
        # Division by zero
        response = client.get("/div?a=10&b=0")
        assert response.status_code == 400
    
    def test_calc_endpoint_all_operations(self, client):
        """Test /calc endpoint with all operations."""
        operations = [
            ("add", 5, 3, 8),
            ("sub", 10, 4, 6),
            ("mul", 6, 7, 42),
            ("div", 20, 4, 5),
        ]
        
        for op, a, b, expected in operations:
            response = client.get(f"/calc?op={op}&a={a}&b={b}")
            assert response.status_code == 200
            assert response.json()["result"] == expected
            assert response.json()["op"] == op
