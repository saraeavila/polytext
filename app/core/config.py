from functools import lru_cache

from pydantic import Field, SecretStr
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

    polytext_admin_key: SecretStr | None = None

    allowed_hosts: str = (
        "localhost,127.0.0.1,testserver"
    )

    cors_allowed_origins: str = ""

    @property
    def is_production(self) -> bool:
        return (
            self.environment.lower()
            == "production"
        )

    @property
    def allowed_hosts_list(
        self,
    ) -> list[str]:
        return [
            host.strip()
            for host in self.allowed_hosts.split(",")
            if host.strip()
        ]

    @property
    def cors_allowed_origins_list(
        self,
    ) -> list[str]:
        return [
            origin.strip()
            for origin
            in self.cors_allowed_origins.split(",")
            if origin.strip()
        ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
