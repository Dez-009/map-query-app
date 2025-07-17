from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database settings - can be set individually or via DB_URL
    DB_URL: str | None = None
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "mapquery" 
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    
    def get_db_url(self) -> str:
        if self.DB_URL:
            return self.DB_URL
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # OpenAI settings
    OPENAI_API_KEY: str = "dummy"
    OPENAI_ASSISTANT_ID: str = "dummy"  # ID of the SQL-specialized assistant
    OPENAI_REQUEST_TIMEOUT: int = 120  # Timeout for OpenAI API requests in seconds (2 minutes)
    OPENAI_MAX_RETRIES: int = 5  # Maximum number of retries for OpenAI API calls

    model_config = {
        "env_file": ".env",
        "case_sensitive": False
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
