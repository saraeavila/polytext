from sqlalchemy import text

from app.core.redis import get_redis_client
from app.db.session import engine


def check_postgres() -> None:
    with engine.connect() as connection:
        connection.execute(
            text("SELECT 1")
        )


def check_redis() -> None:
    redis_client = get_redis_client()

    if not redis_client.ping():
        raise RuntimeError(
            "Redis did not respond to PING."
        )
