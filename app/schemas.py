"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, field_validator, model_validator, ConfigDict
from typing import Optional, Literal


class CalculationCreate(BaseModel):
    """Schema for creating a new calculation."""
    a: float
    b: float
    type: Literal["Add", "Sub", "Multiply", "Divide", "Power", "Modulus"]
    # Note: Literal type provides validation, no need for additional validator

    @model_validator(mode='after')
    def validate_division_by_zero(self):
        """Prevent division by zero and modulus by zero."""
        if self.type == "Divide" and self.b == 0:
            raise ValueError("Division by zero is not allowed")
        if self.type == "Modulus" and self.b == 0:
            raise ValueError("Modulus by zero is not allowed")
        return self


class CalculationRead(BaseModel):
    """Schema for reading a calculation from database."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    a: float
    b: float
    type: str
    result: float
    user_id: Optional[int]


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: str
    username: str
    password: str


class UserRead(BaseModel):
    """Schema for reading user data."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: str
    username: str
    is_active: int


class UserLogin(BaseModel):
    """Schema for user login."""
    username_or_email: str
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    email: Optional[str] = None
    username: Optional[str] = None
    
    @model_validator(mode='after')
    def check_at_least_one_field(self):
        """Ensure at least one field is provided."""
        if not self.email and not self.username:
            raise ValueError("At least one field (email or username) must be provided")
        return self


class PasswordChange(BaseModel):
    """Schema for changing password."""
    current_password: str
    new_password: str
    
    @model_validator(mode='after')
    def validate_new_password(self):
        """Ensure new password is different and meets requirements."""
        if self.current_password == self.new_password:
            raise ValueError("New password must be different from current password")
        if len(self.new_password) < 6:
            raise ValueError("New password must be at least 6 characters long")
        return self


class CalculationStats(BaseModel):
    """Schema for calculation statistics."""
    total_calculations: int
    operations_breakdown: dict
    most_used_operation: Optional[str] = None
    average_result: Optional[float] = None
