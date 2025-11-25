"""SQLAlchemy ORM models."""
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """User model for authentication and ownership."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Integer, default=1)

    # Relationship to calculations
    calculations = relationship("Calculation", back_populates="user")


class Calculation(Base):
    """Calculation model storing arithmetic operations."""
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # Add, Sub, Multiply, Divide
    result = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationship to user
    user = relationship("User", back_populates="calculations")

    def __init__(self, a: float, b: float, type: str, result: float = None, user_id: int = None):
        """Initialize calculation and compute result if not provided."""
        self.a = a
        self.b = b
        self.type = type
        self.user_id = user_id
        
        # Compute result if not provided
        if result is None:
            from app.factory import OperationFactory
            operation = OperationFactory.create(type)
            self.result = operation.compute(a, b)
        else:
            self.result = result
