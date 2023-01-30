import redis  # type: ignore

from src.core import config


def create_redis():
    return redis.ConnectionPool(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)


pool = create_redis()


def get_redis():
    return redis.Redis(connection_pool=pool)
