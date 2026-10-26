from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "BuildLog API"
    environment: str = "development"
    database_url: str = "sqlite:///./backend/buildlog.db"
    test_database_url: str = "sqlite:///:memory:"
    frontend_origin: str = "http://localhost:5173"
    session_secret: str = ""
    admin_email: str = ""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def sqlalchemy_database_url(self) -> str:
        return normalize_database_url(self.database_url)


def normalize_database_url(url: str) -> str:
    """Use psycopg 3 when Supabase provides a standard PostgreSQL URL."""
    if url.startswith("sqlite:///./"):
        relative_path = url.removeprefix("sqlite:///./")
        absolute_path = (PROJECT_ROOT / relative_path).resolve().as_posix()
        return f"sqlite:///{absolute_path}"
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


@lru_cache
def get_settings() -> Settings:
    return Settings()

