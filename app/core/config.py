from functools import lru_cache
from urllib.parse import quote_plus

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

    database_host: str | None = None
    database_port: int = 5432
    database_name: str = "polytext"
    database_user: str | None = None
    database_password: SecretStr | None = None
    database_sslmode: str | None = None

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
    def effective_database_url(self) -> str:
        """Return the database URL for the current deployment environment."""

        if self.database_host is None:
            return self.database_url

        if self.database_user is None or self.database_password is None:
            raise ValueError(
                "DATABASE_USER and DATABASE_PASSWORD are required "
                "when DATABASE_HOST is configured."
            )

        username = quote_plus(self.database_user)
        password = quote_plus(self.database_password.get_secret_value())

        url = (
            f"postgresql+psycopg://{username}:{password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )

        if self.database_sslmode:
            url = f"{url}?sslmode={quote_plus(self.database_sslmode)}"

        return url

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
