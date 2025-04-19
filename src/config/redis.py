from typing import AsyncGenerator

from fastapi_cache import FastAPICache
from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings
from redis.asyncio import Redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry


class RedisSettings(BaseSettings):
    """Redis connection settings with validation and environment variables support."""

    redis_url: RedisDsn = Field(
        default="redis://supermarket-service_redis:6379",
        description="Redis connection URL with schema (redis:// or rediss://)",
        examples=["redis://localhost:6379", "rediss://secure-redis:6379"],
    )
    redis_pool_size: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of connections in the Redis connection pool",
    )
    redis_pool_timeout: int = Field(
        default=5,
        ge=1,
        description="Timeout in seconds for acquiring a connection from the pool",
    )
    redis_cache_ttl: int = Field(
        default=300, ge=60, description="Default TTL (in seconds) for cached items"
    )
    redis_retry_attempts: int = Field(
        default=3,
        ge=0,
        description="Number of retry attempts for failed Redis operations",
    )

    class Config:
        env_prefix = "REDIS_"
        case_sensitive = False
        env_file = ".env"
        extra = "ignore"


async def init_redis_pool(settings: RedisSettings | None = None) -> Redis:
    """Initialize Redis connection pool with retry strategy."""
    if not settings:
        settings = RedisSettings()

    retry_strategy = Retry(
        backoff=ExponentialBackoff(), retries=settings.redis_retry_attempts
    )

    return Redis.from_url(
        str(settings.redis_url),
        encoding="utf8",
        decode_responses=False,  # Important for binary serialization
        max_connections=settings.redis_pool_size,
        socket_timeout=settings.redis_pool_timeout,
        retry_on_timeout=True,
        retry=retry_strategy,
        health_check_interval=30,
    )


async def get_redis() -> AsyncGenerator[Redis, None]:
    """Dependency for getting Redis connection"""
    redis = FastAPICache.get_backend().redis  # type: ignore
    if not redis:
        redis = await init_redis_pool()
    try:
        yield redis
    finally:
        pass  # Don't close the pool here; let lifespan manage it


def get_redis_settings() -> RedisSettings:
    """Get Redis settings with environment variables override."""
    return RedisSettings()
