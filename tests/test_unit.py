"""Unit tests for calculation operations and schemas."""
import pytest
from pydantic import ValidationError
from app.factory import (
    AddOperation,
    SubOperation,
    MultiplyOperation,
    DivideOperation,
    OperationFactory
)
from app.schemas import CalculationCreate


class TestOperationFactory:
    """Test suite for operation factory and individual operations."""
    
    def test_add_operation(self):
        """Test AddOperation computes correct result."""
        op = AddOperation()
        assert op.compute(5, 3) == 8
        assert op.compute(-2, 7) == 5
        assert op.compute(0.1, 0.2) == pytest.approx(0.3)
    
    def test_sub_operation(self):
        """Test SubOperation computes correct result."""
        op = SubOperation()
        assert op.compute(10, 3) == 7
        assert op.compute(5, 10) == -5
        assert op.compute(0, 0) == 0
    
    def test_multiply_operation(self):
        """Test MultiplyOperation computes correct result."""
        op = MultiplyOperation()
        assert op.compute(4, 5) == 20
        assert op.compute(-3, 7) == -21
        assert op.compute(2.5, 4) == 10.0
    
    def test_divide_operation(self):
        """Test DivideOperation computes correct result."""
        op = DivideOperation()
        assert op.compute(10, 2) == 5
        assert op.compute(7, 2) == 3.5
        assert op.compute(-10, 2) == -5
    
    def test_divide_by_zero_raises(self):
        """Test DivideOperation raises on division by zero."""
        op = DivideOperation()
        with pytest.raises(ZeroDivisionError, match="Division by zero"):
            op.compute(10, 0)
    
    def test_factory_creates_add_operation(self):
        """Test factory creates AddOperation."""
        op = OperationFactory.create("Add")
        assert isinstance(op, AddOperation)
        assert op.compute(2, 3) == 5
    
    def test_factory_creates_sub_operation(self):
        """Test factory creates SubOperation."""
        op = OperationFactory.create("Sub")
        assert isinstance(op, SubOperation)
        assert op.compute(10, 3) == 7
    
    def test_factory_creates_multiply_operation(self):
        """Test factory creates MultiplyOperation."""
        op = OperationFactory.create("Multiply")
        assert isinstance(op, MultiplyOperation)
        assert op.compute(4, 5) == 20
    
    def test_factory_creates_divide_operation(self):
        """Test factory creates DivideOperation."""
        op = OperationFactory.create("Divide")
        assert isinstance(op, DivideOperation)
        assert op.compute(10, 2) == 5
    
    def test_factory_invalid_type_raises(self):
        """Test factory raises ValueError for invalid type."""
        with pytest.raises(ValueError, match="Unsupported operation type"):
            OperationFactory.create("Power")


class TestCalculationCreateSchema:
    """Test suite for CalculationCreate Pydantic schema."""
    
    def test_accepts_valid_add(self):
        """Test schema accepts valid Add type."""
        calc = CalculationCreate(a=5, b=3, type="Add")
        assert calc.a == 5
        assert calc.b == 3
        assert calc.type == "Add"
    
    def test_accepts_valid_sub(self):
        """Test schema accepts valid Sub type."""
        calc = CalculationCreate(a=10, b=2, type="Sub")
        assert calc.type == "Sub"
    
    def test_accepts_valid_multiply(self):
        """Test schema accepts valid Multiply type."""
        calc = CalculationCreate(a=4, b=5, type="Multiply")
        assert calc.type == "Multiply"
    
    def test_accepts_valid_divide(self):
        """Test schema accepts valid Divide type."""
        calc = CalculationCreate(a=10, b=2, type="Divide")
        assert calc.type == "Divide"
    
    def test_rejects_invalid_type(self):
        """Test schema rejects invalid operation type."""
        with pytest.raises(ValidationError) as exc_info:
            CalculationCreate(a=5, b=3, type="Power")
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("type" in str(err) for err in errors)
    
    def test_rejects_divide_by_zero(self):
        """Test schema rejects division by zero."""
        with pytest.raises(ValidationError) as exc_info:
            CalculationCreate(a=10, b=0, type="Divide")
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("Division by zero" in str(err) for err in errors)
    
    def test_allows_zero_for_non_divide(self):
        """Test schema allows b=0 for non-divide operations."""
        calc_add = CalculationCreate(a=5, b=0, type="Add")
        assert calc_add.b == 0
        
        calc_mul = CalculationCreate(a=5, b=0, type="Multiply")
        assert calc_mul.b == 0
    
    def test_accepts_floats(self):
        """Test schema accepts float values."""
        calc = CalculationCreate(a=3.14, b=2.71, type="Add")
        assert calc.a == 3.14
        assert calc.b == 2.71
    
    def test_accepts_negative_numbers(self):
        """Test schema accepts negative numbers."""
        calc = CalculationCreate(a=-5, b=-3, type="Sub")
        assert calc.a == -5
        assert calc.b == -3
