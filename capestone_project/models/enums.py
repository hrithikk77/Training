from enum import Enum

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class LoanPurpose(str, Enum):
    personal = "personal"
    education = "education"
    home = "home"
    vehicle = "vehicle"
    business = "business"

class EmploymentStatus(str, Enum):
    employed = "employed"
    self_employed = "self_employed"
    unemployed = "unemployed"
    student = "student"

class LoanStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"