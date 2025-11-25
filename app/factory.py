"""Factory pattern for arithmetic operations."""
from abc import ABC, abstractmethod


class BaseOperation(ABC):
    """Abstract base class for arithmetic operations."""
    
    @abstractmethod
    def compute(self, a: float, b: float) -> float:
        """Compute the operation result."""
        pass  # pragma: no cover - abstract method


class AddOperation(BaseOperation):
    """Addition operation."""
    
    def compute(self, a: float, b: float) -> float:
        """Add two numbers."""
        return a + b


class SubOperation(BaseOperation):
    """Subtraction operation."""
    
    def compute(self, a: float, b: float) -> float:
        """Subtract b from a."""
        return a - b


class MultiplyOperation(BaseOperation):
    """Multiplication operation."""
    
    def compute(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b


class DivideOperation(BaseOperation):
    """Division operation."""
    
    def compute(self, a: float, b: float) -> float:
        """Divide a by b."""
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        return a / b


class OperationFactory:
    """Factory to create operation instances based on type."""
    
    @staticmethod
    def create(type: str) -> BaseOperation:
        """
        Create and return the appropriate operation instance.
        
        Args:
            type: Operation type (Add, Sub, Multiply, Divide)
            
        Returns:
            BaseOperation instance
            
        Raises:
            ValueError: If operation type is not supported
        """
        operations = {
            "Add": AddOperation,
            "Sub": SubOperation,
            "Multiply": MultiplyOperation,
            "Divide": DivideOperation
        }
        
        operation_class = operations.get(type)
        if operation_class is None:
            raise ValueError(f"Unsupported operation type: {type}")
        
        return operation_class()
