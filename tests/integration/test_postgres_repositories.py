from datetime import (
    datetime,
    timedelta,
    timezone,
)
import uuid

import pytest

from app.repositories.api_key import (
    APIKeyRepository,
)
from app.repositories.api_user import (
    APIUserRepository,
)
from app.repositories.request_usage import (
    RequestUsageRepository,
)
from app.security.api_keys import (
    get_api_key_prefix,
    hash_api_key,
)


pytestmark = pytest.mark.integration


def test_user_key_and_usage_persist_to_postgres(
    db,
):
    user_repository = APIUserRepository(db)

    user = user_repository.create(
        name="Integration Sara",
        email="integration@example.com",
    )

    assert user.id is not None
    assert user.email == "integration@example.com"

    plaintext_key = (
        "poly_sk_integration_test_key"
    )

    key_repository = APIKeyRepository(db)

    api_key = key_repository.create(
        user_id=user.id,
        key_prefix=get_api_key_prefix(
            plaintext_key
        ),
        key_hash=hash_api_key(
            plaintext_key
        ),
    )

    assert api_key.id is not None
    assert api_key.user_id == user.id

    found_key = key_repository.get_by_hash(
        hash_api_key(plaintext_key)
    )

    assert found_key is not None
    assert found_key.id == api_key.id

    usage_repository = (
        RequestUsageRepository(db)
    )

    usage = usage_repository.create(
        api_key_id=api_key.id,
        request_id=uuid.uuid4().hex,
        task="sentiment",
        status_code=200,
        latency_ms=42.5,
    )

    assert usage.id is not None
    assert usage.task == "sentiment"

    since = (
        datetime.now(timezone.utc)
        - timedelta(hours=1)
    )

    (
        total,
        successful,
        failed,
        average_latency,
    ) = usage_repository.get_summary_since(
        api_key_id=api_key.id,
        since=since,
    )

    assert total == 1
    assert successful == 1
    assert failed == 0
    assert average_latency == pytest.approx(
        42.5
    )

    task_counts = (
        usage_repository.get_task_counts_since(
            api_key_id=api_key.id,
            since=since,
        )
    )

    assert task_counts == {
        "sentiment": 1,
    }
