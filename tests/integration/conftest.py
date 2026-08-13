import os

import pytest
import redis

from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker

from app.db.models.api_key import APIKey
from app.db.models.api_user import APIUser
from app.db.models.request_usage import RequestUsage


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    (
        "postgresql+psycopg://"
        "polytext:polytext@localhost:5433/polytext_test"
    ),
)

TEST_REDIS_URL = os.getenv(
    "TEST_REDIS_URL",
    "redis://localhost:6380/0",
)


test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
)

TestSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False,
)


@pytest.fixture(
    scope="session",
    autouse=True,
)
def require_integration_tests():
    if os.getenv("RUN_INTEGRATION_TESTS") != "1":
        pytest.skip(
            "Set RUN_INTEGRATION_TESTS=1 "
            "to run integration tests."
        )


def clean_database(db):
    db.execute(delete(RequestUsage))
    db.execute(delete(APIKey))
    db.execute(delete(APIUser))
    db.commit()


@pytest.fixture
def db():
    with TestSessionLocal() as session:
        clean_database(session)

        yield session

        session.rollback()
        clean_database(session)


@pytest.fixture
def redis_client():
    client = redis.Redis.from_url(
        TEST_REDIS_URL,
        decode_responses=True,
    )

    client.flushdb()

    yield client

    client.flushdb()
    client.close()
