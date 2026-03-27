# routers/user_router.py
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from models.schemas import UserCreate, UserLogin, UserResponse
from services.user_service import UserService
from repositories.base_repository import BaseRepository
from repositories.json_repository import JsonRepository
from config import settings

import logging
logger = logging.getLogger(__name__)

# Create an APIRouter instance for user-related endpoints
router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)

# Dependency to get a User Repository instance
def get_user_repository() -> BaseRepository:
    """Provides a singleton instance of the JsonRepository for users."""
    # In a real app, you might have different repository types based on env
    return JsonRepository(settings.USERS_FILE, "users")

# Dependency to get a UserService instance
def get_user_service(user_repo: BaseRepository = Depends(get_user_repository)) -> UserService:
    """Provides a singleton instance of the UserService."""
    return UserService(user_repo)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """
    Registers a new user with the provided username, email, and password.
    Returns the newly created user's public information.
    """
    logger.info(f"Received request to register user: {user_data.username}")
    user = await user_service.register_user(user_data)
    logger.info(f"User '{user.username}' successfully registered.")
    return user

@router.post("/login", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def login_user(
    credentials: UserLogin,
    user_service: UserService = Depends(get_user_service)
):
    """
    Authenticates a user with provided credentials.
    Returns the authenticated user's public information.
    """
    logger.info(f"Received request to login user: {credentials.username}")
    user = await user_service.authenticate_user(credentials)
    # In a real app, a JWT token would be returned here
    logger.info(f"User '{user.username}' successfully logged in.")
    return user

@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def list_users(
    user_service: UserService = Depends(get_user_service)
):
    """
    Retrieves a list of all registered users.
    """
    logger.info("Received request to list all users.")
    users = await user_service.get_all_users()
    logger.info(f"Returning {len(users)} users.")
    return users

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """
    Deletes a user by their ID.
    """
    logger.info(f"Received request to delete user with ID: {user_id}")
    await user_service.delete_user(user_id) # Service raises UserNotFoundError if not found
    logger.info(f"User with ID {user_id} deleted successfully.")
    return {"message": f"User with id {user_id} deleted successfully"}