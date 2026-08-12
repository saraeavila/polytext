from app.services.usage import UsageService


class FakeUsageRepository:
    def __init__(self):
        self.records = []

    def create(
        self,
        api_key_id: int,
        request_id: str,
        task: str,
        status_code: int,
        latency_ms: float,
    ):
        record = {
            "api_key_id": api_key_id,
            "request_id": request_id,
            "task": task,
            "status_code": status_code,
            "latency_ms": latency_ms,
        }

        self.records.append(record)
        return record


def test_usage_service_records_request():
    repository = FakeUsageRepository()
    service = UsageService(repository)

    result = service.record_request(
        api_key_id=1,
        request_id="abc123",
        task="sentiment",
        status_code=200,
        latency_ms=123.45,
    )

    assert result["api_key_id"] == 1
    assert result["task"] == "sentiment"
    assert result["status_code"] == 200
    assert result["latency_ms"] == 123.45
