import aioredis
from aioredis import Redis

from src.core import config


async def get_redis() -> Redis:
    redis: Redis = aioredis.from_url(
        url=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/0",
        max_connections=10,
        encoding="utf8",
        decode_responses=True,
    )
    return redis
