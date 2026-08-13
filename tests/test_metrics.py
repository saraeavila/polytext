from fastapi.testclient import TestClient

from app.main import app


def test_metrics_endpoint():
    with TestClient(app) as client:
        response = client.get(
            "/metrics"
        )

    assert response.status_code == 200

    body = response.text

    assert (
        "polytext_http_requests_total"
        in body
    )

    assert (
        "polytext_http_request_duration_seconds"
        in body
    )

    assert (
        "polytext_model_requests_total"
        in body
    )

    assert (
        "polytext_model_inference_duration_seconds"
        in body
    )

    assert (
        "polytext_rate_limit_rejections_total"
        in body
    )


def test_http_request_is_recorded():
    with TestClient(app) as client:
        health_response = client.get(
            "/health"
        )

        assert (
            health_response.status_code
            == 200
        )

        metrics_response = client.get(
            "/metrics"
        )

    body = metrics_response.text

    assert (
        'route="/health"'
        in body
    )

    assert (
        'status="200"'
        in body
    )
