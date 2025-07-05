from cachetools import TTLCache
from typing import Dict, Any
import hashlib
import json

# Initialize caches
audio_features_cache = TTLCache(maxsize=1000, ttl=600)  # 10 minutes
analysis_cache = TTLCache(maxsize=500, ttl=3600)  # 1 hour

def get_cache_key(prefix: str, data: Any) -> str:
    """Generate a cache key from prefix and data"""
    data_str = json.dumps(data, sort_keys=True)
    return f"{prefix}:{hashlib.md5(data_str.encode()).hexdigest()}"

def get_audio_features_cache_key(track_ids: list) -> str:
    """Generate cache key for audio features"""
    return get_cache_key("audio_features", sorted(track_ids))

def get_analysis_cache_key(track_ids: list, features_hash: str) -> str:
    """Generate cache key for analysis results"""
    return get_cache_key("analysis", {"track_ids": sorted(track_ids), "features": features_hash})

def get_from_cache(cache: TTLCache, key: str) -> Any:
    """Get value from cache"""
    return cache.get(key)

def set_in_cache(cache: TTLCache, key: str, value: Any) -> None:
    """Set value in cache"""
    cache[key] = value 