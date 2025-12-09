"""Unit tests for new operations (Power and Modulus)."""
import pytest
from app import operations


class TestPowerOperation:
    """Test cases for power operation."""
    
    def test_power_positive_numbers(self):
        """Test power with positive numbers."""
        assert operations.power(2, 3) == 8
        assert operations.power(5, 2) == 25
        assert operations.power(10, 0) == 1
    
    def test_power_negative_base(self):
        """Test power with negative base."""
        assert operations.power(-2, 3) == -8
        assert operations.power(-2, 2) == 4
    
    def test_power_negative_exponent(self):
        """Test power with negative exponent."""
        assert operations.power(2, -2) == 0.25
        assert operations.power(10, -1) == 0.1
    
    def test_power_decimal_numbers(self):
        """Test power with decimal numbers."""
        assert operations.power(2.5, 2) == 6.25
        assert abs(operations.power(4, 0.5) - 2.0) < 0.0001  # Square root
    
    def test_power_zero_base(self):
        """Test power with zero base."""
        assert operations.power(0, 5) == 0
        assert operations.power(0, 100) == 0


class TestModulusOperation:
    """Test cases for modulus operation."""
    
    def test_modulus_positive_numbers(self):
        """Test modulus with positive numbers."""
        assert operations.modulus(10, 3) == 1
        assert operations.modulus(15, 4) == 3
        assert operations.modulus(20, 5) == 0
    
    def test_modulus_negative_dividend(self):
        """Test modulus with negative dividend."""
        assert operations.modulus(-10, 3) == 2  # Python's modulo behavior
        assert operations.modulus(-7, 4) == 1
    
    def test_modulus_decimal_numbers(self):
        """Test modulus with decimal numbers."""
        result = operations.modulus(10.5, 3)
        assert abs(result - 1.5) < 0.0001
        
        result = operations.modulus(7.5, 2.5)
        assert abs(result - 0.0) < 0.0001
    
    def test_modulus_by_zero(self):
        """Test modulus by zero raises error."""
        with pytest.raises(ZeroDivisionError):
            operations.modulus(10, 0)
    
    def test_modulus_large_numbers(self):
        """Test modulus with large numbers."""
        assert operations.modulus(1000000, 7) == 1  # 1000000 % 7 = 1
        assert operations.modulus(999999, 1000) == 999


class TestComputeFunction:
    """Test the compute function with new operations."""
    
    def test_compute_power(self):
        """Test compute with Power operation."""
        assert operations.compute(2, 8, "Power") == 256
        assert operations.compute(5, 3, "Power") == 125
    
    def test_compute_modulus(self):
        """Test compute with Modulus operation."""
        assert operations.compute(17, 5, "Modulus") == 2
        assert operations.compute(100, 9, "Modulus") == 1
    
    def test_compute_modulus_by_zero(self):
        """Test compute with Modulus by zero raises error."""
        with pytest.raises(ZeroDivisionError):
            operations.compute(10, 0, "Modulus")
    
    def test_compute_invalid_operation(self):
        """Test compute with invalid operation."""
        with pytest.raises(ValueError):
            operations.compute(5, 3, "InvalidOp")
    
    def test_all_operations(self):
        """Test all supported operations."""
        assert operations.compute(10, 5, "Add") == 15
        assert operations.compute(10, 5, "Sub") == 5
        assert operations.compute(10, 5, "Multiply") == 50
        assert operations.compute(10, 5, "Divide") == 2
        assert operations.compute(10, 5, "Power") == 100000
        assert operations.compute(10, 5, "Modulus") == 0
