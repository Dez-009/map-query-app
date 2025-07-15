import os
try:
    from pydantic_settings import BaseSettings
except ImportError:  # pragma: no cover - fallback for pydantic v1
    from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
