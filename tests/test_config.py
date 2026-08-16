import pytest
from pydantic import SecretStr

from app.core.config import Settings, get_settings


def test_default_settings():
    settings = Settings(
        _env_file=None,
    )

    assert settings.app_name == "PolyText"
    assert settings.environment == "development"
    assert settings.log_level == "INFO"

    assert settings.database_url.startswith(
        "postgresql+psycopg://"
    )

    assert settings.redis_url.startswith(
        "redis://"
    )


def test_settings_can_be_overridden(
    monkeypatch,
):
    monkeypatch.setenv(
        "ENVIRONMENT",
        "testing",
    )

    monkeypatch.setenv(
        "REDIS_URL",
        "redis://example:6379/1",
    )

    settings = Settings(
        _env_file=None,
    )

    assert settings.environment == "testing"

    assert (
        settings.redis_url
        == "redis://example:6379/1"
    )


def test_get_settings_is_cached():
    get_settings.cache_clear()

    first = get_settings()
    second = get_settings()

    assert first is second

    get_settings.cache_clear()


def test_development_is_not_production():
    settings = Settings(
        environment="development"
    )

    assert settings.is_production is False


def test_production_environment():
    settings = Settings(
        environment="production"
    )

    assert settings.is_production is True


def test_allowed_hosts_are_parsed():
    settings = Settings(
        allowed_hosts=(
            "localhost,"
            "127.0.0.1,"
            "api.example.com"
        )
    )

    assert settings.allowed_hosts_list == [
        "localhost",
        "127.0.0.1",
        "api.example.com",
    ]


def test_empty_cors_origins():
    settings = Settings(
        cors_allowed_origins=""
    )

    assert (
        settings.cors_allowed_origins_list
        == []
    )


def test_cors_origins_are_parsed():
    settings = Settings(
        cors_allowed_origins=(
            "https://example.com,"
            "https://app.example.com"
        )
    )

    assert (
        settings.cors_allowed_origins_list
        == [
            "https://example.com",
            "https://app.example.com",
        ]
    )


def test_effective_database_url_uses_database_url_by_default():
    settings = Settings(
        database_url="postgresql+psycopg://user:pass@localhost:5432/polytext"
    )

    assert (
        settings.effective_database_url
        == "postgresql+psycopg://user:pass@localhost:5432/polytext"
    )


def test_effective_database_url_builds_from_components():
    settings = Settings(
        database_host="polytext.example.amazonaws.com",
        database_port=5432,
        database_name="polytext",
        database_user="polytext",
        database_password=SecretStr("secret-password"),
        database_sslmode="require",
    )

    assert settings.effective_database_url == (
        "postgresql+psycopg://polytext:secret-password"
        "@polytext.example.amazonaws.com:5432/polytext"
        "?sslmode=require"
    )


def test_effective_database_url_requires_aws_credentials():
    settings = Settings(
        database_host="polytext.example.amazonaws.com",
        database_user=None,
        database_password=None,
    )

    with pytest.raises(
        ValueError,
        match="DATABASE_USER and DATABASE_PASSWORD",
    ):
        settings.effective_database_url
