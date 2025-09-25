import os
import json
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
_client = None

def get_client():
    global _client
    if _client is None:
        _client = redis.from_url(REDIS_URL, decode_responses=True)
    return _client

def cache_get(key: str):
    return get_client().get(key)

def cache_set(key: str, value, ttl: int = 300):
    if not isinstance(value, str):
        value = json.dumps(value)
    return get_client().setex(key, ttl, value)
