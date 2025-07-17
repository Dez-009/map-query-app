from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "mapquery"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_URL: str = "postgresql://postgres:postgres@db:5432/mapquery"
    
    # OpenAI settings
    OPENAI_API_KEY: str
    OPENAI_ASSISTANT_ID: str  # ID of the SQL-specialized assistant

    model_config = {
        "env_file": ".env"
    }


@lru_cache()
def get_settings() -> Settings:
    return Settings()


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    settings = get_settings()
    print("✅ Loaded settings:")
    print(f"DB_URL = {settings.DB_URL}")
    print(f"OPENAI_API_KEY = {settings.OPENAI_API_KEY[:10]}...")
    print(f"OPENAI_ASSISTANT_ID = {settings.OPENAI_ASSISTANT_ID}")
