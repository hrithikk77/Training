# routers/user_router.py
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from database import get_db
from repositories.sqlalchemy_repository import SqlAlchemyRepository
from models.schemas import UserCreate, UserLogin, UserResponse
from services.user_service import UserService
from repositories.base_repository import BaseRepository
# from repositories.json_repository import JsonRepository
from config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from models.db_models import User

import logging
logger = logging.getLogger(__name__)

# Create an APIRouter instance for user-related endpoints
router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)

# Dependency to get a User Repository instance
def get_user_repository(db: AsyncSession = Depends(get_db)) -> BaseRepository:
    return SqlAlchemyRepository(db, User)

def get_user_service(user_repo: BaseRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repo)

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserCreate, service: UserService = Depends(get_user_service)):
    # This now matches the service name above
    return await service.register_user(data)

@router.post("/login", response_model=UserResponse)
async def login(data: UserLogin, service: UserService = Depends(get_user_service)):
    # This now matches the service name above
    return await service.authenticate_user(data)

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