"""
Multi-Layer Caching Engine for India Cost of Living Index.
Provides high-performance Redis caching with automatic in-memory LRU fallback.
"""
import json
import logging
from typing import Any, Optional, Dict, Tuple

logger = logging.getLogger(__name__)


class MultiLayerCacheEngine:
    """
    Tries Redis first. If Redis is unavailable or fails, falls back 
    seamlessly to an in-memory LRU dictionary cache.
    """

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, max_lru_size: int = 512):
        self.max_lru_size = max_lru_size
        self._in_memory_cache: Dict[str, Any] = {}
        self.redis_client = None
        self.using_redis = False

        # Only attempt Redis connection if explicitly configured
        import os
        use_redis = os.environ.get("USE_REDIS", "false").lower() in ("true", "1")
        redis_env_host = os.environ.get("REDIS_HOST")
        
        if use_redis or redis_env_host:
            host = redis_env_host if redis_env_host else "127.0.0.1"
            try:
                import redis
                client = redis.Redis(
                    host=host, 
                    port=port, 
                    db=db, 
                    socket_timeout=0.2,
                    socket_connect_timeout=0.2
                )
                client.ping()
                self.redis_client = client
                self.using_redis = True
                logger.info("Connected to Redis cache successfully.")
            except Exception:
                logger.info("Redis not reachable. Using in-memory LRU cache.")
                self.redis_client = None
                self.using_redis = False
        else:
            self.redis_client = None
            self.using_redis = False

    def get(self, key: str) -> Optional[Any]:
        """Retrieve item from Redis or In-Memory cache."""
        if self.using_redis and self.redis_client:
            try:
                val = self.redis_client.get(key)
                if val:
                    return json.loads(val.decode('utf-8'))
            except Exception:
                pass
                
        return self._in_memory_cache.get(key, None)

    def set(self, key: str, value: Any, ttl_seconds: int = 3600):
        """Set item in Redis and/or In-Memory cache."""
        if self.using_redis and self.redis_client:
            try:
                self.redis_client.setex(key, ttl_seconds, json.dumps(value))
            except Exception:
                pass

        # In-memory LRU maintenance
        if len(self._in_memory_cache) >= self.max_lru_size:
            # Evict oldest entry
            self._in_memory_cache.pop(next(iter(self._in_memory_cache)))
        self._in_memory_cache[key] = value

    def clear(self):
        """Clear cache."""
        self._in_memory_cache.clear()
        if self.using_redis and self.redis_client:
            try:
                self.redis_client.flushdb()
            except Exception:
                pass
