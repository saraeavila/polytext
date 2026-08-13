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
