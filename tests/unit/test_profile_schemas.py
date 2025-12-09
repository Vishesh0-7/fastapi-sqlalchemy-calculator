"""Unit tests for profile and password management."""
import pytest
from app import crud, schemas
from app.security import hash_password, verify_password


class TestPasswordHashing:
    """Test password hashing and verification."""
    
    def test_hash_password_creates_hash(self):
        """Test that password hashing creates a hash."""
        password = "mypassword123"
        hashed = hash_password(password)
        
        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 0
    
    def test_hash_password_different_hashes(self):
        """Test that same password produces different hashes (due to salt)."""
        password = "mypassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Hashes should be different due to different salts
        assert hash1 != hash2
    
    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "mypassword123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "mypassword123"
        hashed = hash_password(password)
        
        assert verify_password("wrongpassword", hashed) is False
    
    def test_verify_password_case_sensitive(self):
        """Test that password verification is case-sensitive."""
        password = "MyPassword123"
        hashed = hash_password(password)
        
        assert verify_password("mypassword123", hashed) is False


class TestPasswordChangeSchema:
    """Test PasswordChange schema validation."""
    
    def test_password_change_valid(self):
        """Test valid password change data."""
        data = {
            "current_password": "oldpass123",
            "new_password": "newpass456"
        }
        schema = schemas.PasswordChange(**data)
        
        assert schema.current_password == "oldpass123"
        assert schema.new_password == "newpass456"
    
    def test_password_change_same_password(self):
        """Test that new password must be different."""
        with pytest.raises(ValueError, match="must be different"):
            schemas.PasswordChange(
                current_password="samepass",
                new_password="samepass"
            )
    
    def test_password_change_too_short(self):
        """Test that new password must be at least 6 characters."""
        with pytest.raises(ValueError, match="at least 6 characters"):
            schemas.PasswordChange(
                current_password="oldpass",
                new_password="short"
            )
    
    def test_password_change_minimum_length(self):
        """Test password with exactly 6 characters is valid."""
        schema = schemas.PasswordChange(
            current_password="oldpass",
            new_password="pass12"
        )
        assert schema.new_password == "pass12"


class TestUserUpdateSchema:
    """Test UserUpdate schema validation."""
    
    def test_user_update_email_only(self):
        """Test updating email only."""
        schema = schemas.UserUpdate(email="newemail@example.com")
        assert schema.email == "newemail@example.com"
        assert schema.username is None
    
    def test_user_update_username_only(self):
        """Test updating username only."""
        schema = schemas.UserUpdate(username="newusername")
        assert schema.username == "newusername"
        assert schema.email is None
    
    def test_user_update_both_fields(self):
        """Test updating both email and username."""
        schema = schemas.UserUpdate(
            email="newemail@example.com",
            username="newusername"
        )
        assert schema.email == "newemail@example.com"
        assert schema.username == "newusername"
    
    def test_user_update_no_fields(self):
        """Test that at least one field must be provided."""
        with pytest.raises(ValueError, match="At least one field"):
            schemas.UserUpdate()
    
    def test_user_update_empty_strings(self):
        """Test that empty strings are treated as no field provided."""
        with pytest.raises(ValueError, match="At least one field"):
            schemas.UserUpdate(email="", username="")


class TestCalculationStatsSchema:
    """Test CalculationStats schema."""
    
    def test_calculation_stats_complete(self):
        """Test stats with complete data."""
        data = {
            "total_calculations": 10,
            "operations_breakdown": {"Add": 5, "Multiply": 5},
            "most_used_operation": "Add",
            "average_result": 42.5
        }
        schema = schemas.CalculationStats(**data)
        
        assert schema.total_calculations == 10
        assert schema.operations_breakdown == {"Add": 5, "Multiply": 5}
        assert schema.most_used_operation == "Add"
        assert schema.average_result == 42.5
    
    def test_calculation_stats_no_calculations(self):
        """Test stats with no calculations."""
        data = {
            "total_calculations": 0,
            "operations_breakdown": {},
            "most_used_operation": None,
            "average_result": None
        }
        schema = schemas.CalculationStats(**data)
        
        assert schema.total_calculations == 0
        assert schema.operations_breakdown == {}
        assert schema.most_used_operation is None
        assert schema.average_result is None


class TestCalculationCreateSchemaNewOperations:
    """Test CalculationCreate schema with new operations."""
    
    def test_power_operation_valid(self):
        """Test Power operation is valid."""
        schema = schemas.CalculationCreate(a=2, b=3, type="Power")
        assert schema.type == "Power"
    
    def test_modulus_operation_valid(self):
        """Test Modulus operation is valid."""
        schema = schemas.CalculationCreate(a=10, b=3, type="Modulus")
        assert schema.type == "Modulus"
    
    def test_modulus_by_zero_validation(self):
        """Test modulus by zero is caught by validation."""
        with pytest.raises(ValueError, match="Modulus by zero"):
            schemas.CalculationCreate(a=10, b=0, type="Modulus")
    
    def test_all_operations_valid(self):
        """Test all operation types are valid."""
        operations = ["Add", "Sub", "Multiply", "Divide", "Power", "Modulus"]
        
        for op in operations:
            if op in ["Divide", "Modulus"]:
                schema = schemas.CalculationCreate(a=10, b=2, type=op)
            else:
                schema = schemas.CalculationCreate(a=10, b=0, type=op)
            assert schema.type == op
    
    def test_invalid_operation_type(self):
        """Test invalid operation type is rejected."""
        with pytest.raises(ValueError):
            schemas.CalculationCreate(a=10, b=5, type="InvalidOperation")
