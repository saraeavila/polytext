from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PolyText"
    environment: str = "development"
    log_level: str = "INFO"

    database_url: str = (
        "postgresql+psycopg://"
        "polytext:polytext@localhost:5432/polytext"
    )

    redis_url: str = "redis://localhost:6379/0"

    fasttext_model_path: str = (
        "resources/models/lid.176.ftz"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
