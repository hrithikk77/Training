import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"
    )

    APP_NAME: str = "TaskAPI"
    DATABASE_URL: str
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "logs/app.log"

settings = Settings()