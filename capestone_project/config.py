from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "LoanHub"
    DATABASE_URL: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ADMIN_EMAIL: str
    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10
    
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # This setting tells Pydantic to ignore extra fields if they exist 
    # and load from .env
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()