from pydantic import BaseModel


class TaskUsage(BaseModel):
    task: str
    requests: int


class UsageSummaryResponse(BaseModel):
    api_key_id: int
    period_hours: int

    total_requests: int
    successful_requests: int
    failed_requests: int

    average_latency_ms: float | None

    tasks: list[TaskUsage]
