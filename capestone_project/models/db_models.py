from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from .enums import UserRole, LoanPurpose, LoanStatus, EmploymentStatus

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "LoanHub"}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=False)
    monthly_income = Column(Integer, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    loans = relationship("Loan", back_populates="owner")


class Loan(Base):
    __tablename__ = "loans"
    __table_args__ = {"schema": "LoanHub"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("LoanHub.users.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    purpose = Column(Enum(LoanPurpose), nullable=False)
    tenure_months = Column(Integer, nullable=False)
    employment_status = Column(Enum(EmploymentStatus), nullable=False)
    status = Column(Enum(LoanStatus), default=LoanStatus.pending)
    admin_remarks = Column(Text, nullable=True)
    reviewed_by = Column(String(50), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    credit_score = Column(Integer, nullable=True)

    owner = relationship("User", back_populates="loans")