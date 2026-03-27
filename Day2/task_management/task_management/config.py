# config.py
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.
    """
    # For Pydantic v2+, use SettingsConfigDict
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "Task Management API"
    APP_VERSION: str = "1.0.0"
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_GOES_HERE" # <<< IMPORTANT: CHANGE THIS IN PRODUCTION!
    ALGORITHM: str = "HS256" # Algorithm for JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # How long JWT tokens are valid

    DATA_PATH: str = "data"
    TASKS_FILE: str = os.path.join(DATA_PATH, "tasks.json")
    USERS_FILE: str = os.path.join(DATA_PATH, "users.json")

    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "logs/app.log"
    LOG_FILE_SIZE_MB: int = 5
    LOG_BACKUP_COUNT: int = 3

    # Derived property for the full log file path
    @property
    def full_log_file_path(self):
        # Using os.path.join ensures cross-platform compatibility
        return os.path.abspath(self.LOG_FILE_PATH)

# Create a single instance of settings to be imported throughout the application
settings = Settings()