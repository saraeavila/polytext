from redis import Redis


RATE_LIMIT_SCRIPT = """
local count = redis.call("INCR", KEYS[1])

if count == 1 then
    redis.call("EXPIRE", KEYS[1], ARGV[1])
end

local ttl = redis.call("TTL", KEYS[1])

return {count, ttl}
"""


class RedisRateLimitRepository:
    def __init__(
        self,
        client: Redis,
        window_seconds: int = 60,
    ):
        self._client = client
        self._window_seconds = window_seconds

        self._script = client.register_script(
            RATE_LIMIT_SCRIPT
        )

    def increment(
        self,
        api_key_id: int,
    ) -> tuple[int, int]:
        key = f"polytext:rate_limit:{api_key_id}"

        result = self._script(
            keys=[key],
            args=[self._window_seconds],
        )

        count = int(result[0])
        ttl = max(int(result[1]), 1)

        return count, ttl
