import redis
from redis import Redis

from core import settings


def get_redis_connection() -> Redis:
    return redis.Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db,
    )
