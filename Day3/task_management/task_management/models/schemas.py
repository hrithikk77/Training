from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, validator
from models.enums import TaskStatus, TaskPriority

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

class UserCreate(BaseSchema):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserLogin(BaseSchema):
    username: str
    password: str

class UserResponse(BaseSchema):
    id: int
    username: str
    email: str
    created_at: datetime

    @validator('email')
    def mask_email(cls, v):
        if "@" in v:
            name, domain = v.split("@")
            return f"{name[:2]}***@{domain}"
        return v

# --- Task Schemas ---
class TaskCreate(BaseSchema):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: TaskPriority = TaskPriority.MEDIUM
    owner: str

class TaskUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None

class TaskResponse(BaseSchema):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    owner: str
    created_at: datetime
    updated_at: datetime