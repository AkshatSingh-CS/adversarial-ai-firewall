"""
Simple in-memory cache with TTL support.

This cache is intended for:
- Prompt hash caching
- Semantic inference caching
- Temporary security state

Later it can be replaced by Redis without changing
the rest of the application.
"""

from __future__ import annotations

import time
from typing import Any


class MemoryCache:
    """Simple TTL cache."""

    def __init__(self) -> None:
        self._cache: dict[str, tuple[Any, float]] = {}

    def set(
        self,
        key: str,
        value: Any,
        ttl: int = 300,
    ) -> None:
        """
        Store an item in the cache.

        Args:
            key: Cache key.
            value: Cached value.
            ttl: Time-to-live in seconds.
        """
        expiry = time.time() + ttl
        self._cache[key] = (value, expiry)

    def get(self, key: str) -> Any | None:
        """
        Retrieve an item from the cache.

        Returns:
            Cached value or None if missing/expired.
        """
        item = self._cache.get(key)

        if item is None:
            return None

        value, expiry = item

        if expiry < time.time():
            del self._cache[key]
            return None

        return value

    def delete(self, key: str) -> None:
        """Delete an item from the cache."""
        self._cache.pop(key, None)

    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()

    def size(self) -> int:
        """Return the number of active cache entries."""
        return len(self._cache)


cache = MemoryCache()