from passlib.context import CryptContext
from models.schemas import UserCreate, UserLogin
from exceptions.custom_exceptions import DuplicateUserError, InvalidCredentialsError
from repositories.base_repository import BaseRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, repo: BaseRepository):
        self.repo = repo

    # RENAMED from 'register' to 'register_user'
    async def register_user(self, data: UserCreate):
        if await self.repo.find_one_by_field("username", data.username):
            raise DuplicateUserError(f"Username '{data.username}' is already taken")
        
        user_dict = data.model_dump()
        user_dict["password"] = pwd_context.hash(data.password)
        return await self.repo.create(user_dict)

    # RENAMED to match Day 2 style
    async def authenticate_user(self, data: UserLogin):
        user = await self.repo.find_one_by_field("username", data.username)
        if not user or not pwd_context.verify(data.password, user["password"]):
            raise InvalidCredentialsError()
        return user

    async def get_all_users(self):
        return await self.repo.get_all()