import os
try:
    from pydantic_settings import BaseSettings
except ImportError:  # pragma: no cover - fallback for pydantic v1
    from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database settings
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    
    # OpenAI settings
    OPENAI_API_KEY: str
    OPENAI_ASSISTANT_ID: str  # ID of the SQL-specialized assistant

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    settings = get_settings()
    print("✅ Loaded settings:")
    print(f"DB_HOST = {settings.DB_HOST}")
    print(f"DB_PORT = {settings.DB_PORT}")
    print(f"DB_NAME = {settings.DB_NAME}")
    print(f"DB_USER = {settings.DB_USER}")
    print(f"DB_PASSWORD = {settings.DB_PASSWORD}")
    print(f"OPENAI_API_KEY = {settings.OPENAI_API_KEY[:10]}...")
    print(f"OPENAI_ASSISTANT_ID = {settings.OPENAI_ASSISTANT_ID}")
