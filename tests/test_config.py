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
