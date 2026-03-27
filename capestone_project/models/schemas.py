from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from .enums import LoanPurpose, EmploymentStatus, LoanStatus

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone: str
    monthly_income: int

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    class Config: from_attributes = True

class LoanCreate(BaseModel):
    amount: int
    purpose: LoanPurpose
    tenure_months: int
    employment_status: EmploymentStatus

class LoanReview(BaseModel):
    status: LoanStatus
    admin_remarks: str = Field(..., min_length=5)

class LoanResponse(BaseModel):
    id: int
    amount: int
    purpose: LoanPurpose
    status: LoanStatus
    applied_at: datetime
    admin_remarks: Optional[str]
    reviewed_by: Optional[str]
    class Config: from_attributes = True



class LoanCreate(BaseModel):
    # Matches: amount, purpose, tenure_months, employment_status
    amount: int = Field(..., gt=0, le=1000000)
    purpose: LoanPurpose
    tenure_months: int = Field(..., ge=6, le=360)
    employment_status: EmploymentStatus

class LoanReview(BaseModel):
    # Matches: status, admin_remarks
    status: LoanStatus 
    admin_remarks: str = Field(..., min_length=5, max_length=500)
