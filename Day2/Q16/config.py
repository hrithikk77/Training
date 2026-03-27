from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool
    JSON_DB_PATH: str
    LOG_LEVEL: str

    model_config = SettingsConfigDict(env_file=".env")


#  Singleton instance
settings = Settings()
