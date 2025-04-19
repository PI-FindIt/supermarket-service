from typing import Any, AsyncGenerator, Callable, TypeVar
from redis.asyncio import Redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from pydantic_settings import BaseSettings

T = TypeVar("T")

class RedisSettings(BaseSettings):
    """Redis connection settings"""
    # TODO THIS MUST BE SET IN THE COMPOSE FILE and get from env
    redis_url: str = "redis://supermarket-service_redis:6379"
    redis_pool_size: int = 10
    redis_pool_timeout: int = 5
    redis_pool_retry_attempts: int = 3

    class Config:
        env_prefix = "REDIS_"

async def init_redis_pool() -> Redis:
    """Initialize Redis connection pool"""
    settings = RedisSettings()
    redis = Redis.from_url(
        settings.redis_url,
        encoding="utf8",
        decode_responses=True,
        max_connections=settings.redis_pool_size,
        socket_timeout=settings.redis_pool_timeout,
        retry_on_timeout=True,
        retry=settings.redis_pool_retry_attempts
    )
    try:
        await redis.ping()
        return redis
    except Exception as e:
        raise Exception(f"Could not connect to Redis: {str(e)}")

async def get_redis() -> AsyncGenerator[Redis, None]:
    """Dependency for getting Redis connection"""
    redis = await init_redis_pool()
    try:
        yield redis
    finally:
        await redis.close()

async def setup_redis_cache() -> None:
    """Initialize FastAPI Cache with Redis backend"""
    redis = await init_redis_pool()
    FastAPICache.init(
        RedisBackend(redis), 
        prefix="supermarket-cache",
        key_builder=None,
        expire=None
    )

def cached_resolver(
    expire: int = 600,  # 10 minutes default (600 seconds)
    namespace: str | None = None
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Cache decorator for GraphQL resolvers
    :param expire: Cache expiration time in seconds
    :param namespace: Cache namespace for grouping related items
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            cache_key_args = args[1:] if args else ()
            return await cache(
                expire=expire,
                namespace=namespace,
                key_builder=lambda: f"{func.__name__}:{str(cache_key_args)}:{str(kwargs)}"
            )(func)(*args, **kwargs)
        return wrapper
    return decorator
