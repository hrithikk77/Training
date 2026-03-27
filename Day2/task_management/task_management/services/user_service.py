# services/user_service.py
from datetime import datetime
from typing import List, Dict, Any, Optional
from passlib.context import CryptContext # For password hashing
import hashlib

from models.schemas import UserCreate, UserLogin, UserResponse
from repositories.base_repository import BaseRepository
from exceptions.custom_exceptions import DuplicateUserError, UserNotFoundError, InvalidCredentialsError

import logging
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    """
    Handles user-related business logic, including creation, retrieval,
    and authentication. Depends on an abstract BaseRepository.
    Adheres to SRP (only user business logic) and DIP (depends on abstraction).
    """

    def __init__(self, user_repository: BaseRepository):
        self.user_repository = user_repository

    def get_password_hash(self, password: str) -> str:
        """Hashes a plain-text password using SHA256 pre-hash + bcrypt.
        Bcrypt has a 72-byte limit, so we pre-hash with SHA256 to handle
        longer passwords while maintaining security.
        """
        # Pre-hash with SHA256 to handle passwords longer than 72 bytes
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return pwd_context.hash(password_hash)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifies a plain-text password against a hashed password.
        
        Pre-hashes the plain password with SHA256 before verifying with bcrypt,
        matching the hashing process used during registration.
        """
        # Pre-hash with SHA256 to match what we did during registration
        password_hash = hashlib.sha256(plain_password.encode()).hexdigest()
        return pwd_context.verify(password_hash, hashed_password)

    async def register_user(self, user_data: UserCreate) -> UserResponse:
        """
        Registers a new user after checking for duplicates.
        Hashes the password before storing.
        """
        existing_user_by_username = await self.user_repository.find_one_by_field("username", user_data.username)
        if existing_user_by_username:
            logger.warning(f"Attempted registration with duplicate username: {user_data.username}")
            raise DuplicateUserError(f"User with username '{user_data.username}' already exists.")

        existing_user_by_email = await self.user_repository.find_one_by_field("email", user_data.email)
        if existing_user_by_email:
            logger.warning(f"Attempted registration with duplicate email: {user_data.email}")
            raise DuplicateUserError(f"User with email '{user_data.email}' already exists.")

        hashed_password = self.get_password_hash(user_data.password)

        user_to_create_dict = user_data.model_dump() 
        user_to_create_dict["password"] = hashed_password

        created_user_dict = await self.user_repository.create(user_to_create_dict)
        logger.info(f"User '{created_user_dict.get('username')}' registered with ID {created_user_dict.get('id')}.")
        return UserResponse(**created_user_dict)

    async def authenticate_user(self, credentials: UserLogin) -> Optional[UserResponse]:
        """
        Authenticates a user by verifying username and password.
        """
        
        user_in_db = await self.user_repository.find_one_by_field("username", credentials.username)
        if not user_in_db:
            logger.warning(f"Login attempt failed for non-existent username: {credentials.username}")
            raise InvalidCredentialsError()

        if not self.verify_password(credentials.password, user_in_db["password"]):
            logger.warning(f"Login attempt failed for user '{credentials.username}' with incorrect password.")
            raise InvalidCredentialsError()

        logger.info(f"User '{credentials.username}' authenticated successfully.")
        return UserResponse(**user_in_db)

    async def get_all_users(self) -> List[UserResponse]:
        """
        Retrieves all registered users.
        """
        users_in_db = await self.user_repository.get_all()
        return [UserResponse(**user) for user in users_in_db]

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        """
        Retrieves a user by their ID.
        """
        user_in_db = await self.user_repository.get_by_id(user_id)
        if not user_in_db:
            logger.warning(f"Attempted to retrieve non-existent user with ID: {user_id}")
            raise UserNotFoundError(user_id)
        return UserResponse(**user_in_db)

    async def get_user_by_username(self, username: str) -> UserResponse:
        """
        Retrieves a user by their username.
        """
        user_in_db = await self.user_repository.find_one_by_field("username", username)
        if not user_in_db:
            logger.warning(f"Attempted to retrieve non-existent user with username: {username}")
            # For security, avoid distinguishing between "username not found" and "wrong password"
            # on login, but for internal user lookup, it's fine.
            raise UserNotFoundError(username) # Here, using username as the identifier for the exception
        return UserResponse(**user_in_db)

    async def delete_user(self, user_id: int) -> bool:
        """
        Deletes a user by their ID.
        """
        # First, check if the user exists
        user_exists = await self.user_repository.get_by_id(user_id)
        if not user_exists:
            logger.warning(f"Attempted to delete non-existent user with ID: {user_id}")
            raise UserNotFoundError(user_id)

        is_deleted = await self.user_repository.delete(user_id)
        if is_deleted:
            logger.info(f"User with ID {user_id} deleted successfully.")
        else:
            logger.error(f"Failed to delete user with ID {user_id} even after existence check.")
        return is_deleted