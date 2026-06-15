from pydantic_settings import BaseSettings
from pathlib import Path

# Caminho absoluto até à pasta .envs
ENV_PATH = Path(__file__).resolve().parents[2] / ".envs" / ".env"

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ANTHROPIC_API_KEY: str
    ENVIRONMENT: str = "development"

    class Config:
        env_file = str(ENV_PATH)
        env_file_encoding = "utf-8"

settings = Settings()
