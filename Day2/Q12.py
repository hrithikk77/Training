# Q12. Pydantic — User Schema with Nested Validation 

# Topics: Pydantic, Nested Models, Validation 

# Problem Statement: 

# Create Pydantic models: Address (street, city, zip_code), UserCreate (username, email, password, age, address). Add validations: email must contain '@', password min 8 chars, age 18-120, zip_code must be exactly 6 digits. Create UserResponse that excludes password. 

# Input: 

# data = {"username": "alice", "email": "alice@mail.com", 

#   "password": "securepass", "age": 25, 

#   "address": {"street": "MG Road", "city": "Bangalore", "zip_code": "560001"}} 

# user = UserCreate(**data) 

# print(UserResponse(**user.model_dump())) 

# Output: 

# username='alice' email='alice@mail.com' age=25 address=Address(...) 

# Constraints: 

# Use field_validator or Field() constraints 

# Invalid data must raise ValidationError with clear messages 

# UserResponse must NOT include password field 

# Use model_dump() for serialization 






from pydantic import BaseModel, Field, field_validator, ValidationError
import re


# 1 Address Model
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

    @field_validator("zip_code")
    @classmethod
    def validate_zip(cls, v):
        if not re.fullmatch(r"\d{6}", v):
            raise ValueError("zip_code must be exactly 6 digits")
        return v


# 2 UserCreate Model
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    age: int
    address: Address  # Nested model

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("age")
    @classmethod
    def validate_age(cls, v):
        if v < 18 or v > 120:
            raise ValueError("Age must be between 18 and 120")
        return v


# 3 UserResponse Model (NO password)
class UserResponse(BaseModel):
    username: str
    email: str
    age: int
    address: Address


data = {
    "username": "alice",
    "email": "alice@mail.com",
    "password": "securepass",
    "age": 25,
    "address": {
        "street": "MG Road",
        "city": "Bangalore",
        "zip_code": "560001"
    }
}

try:
    user = UserCreate(**data)

    # Convert to response (exclude password)
    response = UserResponse(**user.model_dump())
    print(response)

except ValidationError as e:
    print(e)