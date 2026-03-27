# models/schemas.py
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, validator, root_validator
# Note: root_validator is for Pydantic v1. For Pydantic v2+, use model_validator(mode='after')

from models.enums import TaskStatus, TaskPriority

# --- Base Models (for common fields and inheritance) ---
class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    class Config:
        from_attributes = True  # Renamed from orm_mode for Pydantic v2+

# --- User Schemas ---
class UserCreate(BaseSchema):
    """Schema for creating a new user."""
    username: str = Field(..., min_length=3, max_length=30, example="john_doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., min_length=8, example="StrongPassword123")

class UserLogin(BaseSchema):
    """Schema for user login credentials."""
    username: str = Field(..., example="john_doe")
    password: str = Field(..., example="StrongPassword123")


class UserResponse(BaseSchema):
    """Schema for responding with user data (excluding password)."""
    id: int = Field(..., example=1)
    username: str = Field(..., example="john_doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    created_at: datetime = Field(..., example="2023-10-27T10:00:00.000Z")


# --- Task Schemas ---
class TaskCreate(BaseSchema):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=3, max_length=100, example="Buy groceries")
    description: Optional[str] = Field(None, max_length=500, example="Milk, eggs, bread")
    priority: TaskPriority = Field(TaskPriority.MEDIUM, example=TaskPriority.MEDIUM)
    # status defaults to pending, but we won't allow setting it during creation for simplicity
    # The service layer will set the initial status.
    owner: str = Field(..., min_length=3, max_length=30, example="john_doe") # Owner required on creation

class TaskUpdate(BaseSchema):
    """Schema for updating an existing task (partial update allowed)."""
    title: Optional[str] = Field(None, min_length=3, max_length=100, example="Buy fruits")
    description: Optional[str] = Field(None, max_length=500, example="Apples, bananas, oranges")
    status: Optional[TaskStatus] = Field(None, example=TaskStatus.IN_PROGRESS)
    priority: Optional[TaskPriority] = Field(None, example=TaskPriority.HIGH)
    # owner: Optional[str] = Field(None, min_length=3, max_length=30, example="john_doe") # Owner cannot be changed directly via update, only internally

    @validator('title', 'description', 'status', 'priority', pre=True, always=True)
    def check_empty_strings(cls, v):
        if isinstance(v, str) and not v.strip():
            # Convert empty/whitespace-only strings to None for optional fields
            return None
        return v

class TaskResponse(BaseSchema):
    """Schema for responding with task data."""
    id: int = Field(..., example=1)
    title: str = Field(..., example="Buy groceries")
    description: Optional[str] = Field(None, example="Milk, eggs, bread")
    status: TaskStatus = Field(..., example=TaskStatus.PENDING)
    priority: TaskPriority = Field(..., example=TaskPriority.MEDIUM)
    owner: str = Field(..., example="john_doe")
    created_at: datetime = Field(..., example="2023-10-27T10:00:00.000Z")
    updated_at: datetime = Field(..., example="2023-10-27T10:30:00.000Z")

# --- Token Schemas (for authentication, will be used later) ---
class Token(BaseSchema):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseSchema):
    username: Optional[str] = None