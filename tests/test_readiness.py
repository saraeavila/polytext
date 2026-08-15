from fastapi.testclient import TestClient

from app.main import app


def test_ready_when_dependencies_are_available(
    monkeypatch,
):
    monkeypatch.setattr(
        "app.api.routes.readiness.check_postgres",
        lambda: None,
    )

    monkeypatch.setattr(
        "app.api.routes.readiness.check_redis",
        lambda: None,
    )

    with TestClient(app) as client:
        response = client.get(
            "/ready"
        )

    assert response.status_code == 200

    assert response.json() == {
        "status": "ready",
        "checks": {
            "postgres": "ready",
            "redis": "ready",
        },
    }


def test_not_ready_when_postgres_is_unavailable(
    monkeypatch,
):
    def postgres_failure():
        raise RuntimeError(
            "database unavailable"
        )

    monkeypatch.setattr(
        "app.api.routes.readiness.check_postgres",
        postgres_failure,
    )

    monkeypatch.setattr(
        "app.api.routes.readiness.check_redis",
        lambda: None,
    )

    with TestClient(app) as client:
        response = client.get(
            "/ready"
        )

    assert response.status_code == 503

    assert response.json() == {
        "status": "not_ready",
        "checks": {
            "postgres": "unavailable",
            "redis": "ready",
        },
    }


def test_not_ready_when_redis_is_unavailable(
    monkeypatch,
):
    def redis_failure():
        raise RuntimeError(
            "redis unavailable"
        )

    monkeypatch.setattr(
        "app.api.routes.readiness.check_postgres",
        lambda: None,
    )

    monkeypatch.setattr(
        "app.api.routes.readiness.check_redis",
        redis_failure,
    )

    with TestClient(app) as client:
        response = client.get(
            "/ready"
        )

    assert response.status_code == 503

    assert response.json() == {
        "status": "not_ready",
        "checks": {
            "postgres": "ready",
            "redis": "unavailable",
        },
    }


def test_not_ready_when_all_dependencies_are_unavailable(
    monkeypatch,
):
    def failure():
        raise RuntimeError(
            "dependency unavailable"
        )

    monkeypatch.setattr(
        "app.api.routes.readiness.check_postgres",
        failure,
    )

    monkeypatch.setattr(
        "app.api.routes.readiness.check_redis",
        failure,
    )

    with TestClient(app) as client:
        response = client.get(
            "/ready"
        )

    assert response.status_code == 503

    assert response.json() == {
        "status": "not_ready",
        "checks": {
            "postgres": "unavailable",
            "redis": "unavailable",
        },
    }
