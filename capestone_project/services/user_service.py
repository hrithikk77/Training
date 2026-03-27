from sqlalchemy.orm import Session
from models.db_models import User
from models.schemas import UserCreate
from utils.auth_utils import hash_password, verify_password, create_access_token
from exceptions.custom_exceptions import DuplicateUserError, InvalidCredentialsError
from decorators.timer import timer

class UserService:
    @staticmethod
    @timer
    def register_user(db: Session, user_in: UserCreate):
        # Rule: Email and Username must be unique
        check_user = db.query(User).filter(
            (User.email == user_in.email) | (User.username == user_in.username)
        ).first()
        
        if check_user:
            raise DuplicateUserError("Username or Email already exists")

        new_user = User(
            username=user_in.username,
            email=user_in.email,
            password=hash_password(user_in.password),                                                                                             
            phone=user_in.phone,
            monthly_income=user_in.monthly_income
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    @timer
    def login_user(db: Session, username, password):
        user = db.query(User).filter(User.username == username).first()
        
        if not user or not verify_password(password, user.password):
            raise InvalidCredentialsError("Invalid username or password")

        # Create the JWT "ID Card"
        token = create_access_token(data={
            "sub": user.username, 
            "role": user.role.value,
            "id": user.id
        })
        return {"access_token": token, "token_type": "bearer"}