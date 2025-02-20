from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class Cache:
    def __init__(self):
        self._cache = {}

    def get(self, key: str):
        data = self._cache.get(key)
        if data and data["expire"] > datetime.now():
            logger.info(f"Данные из кеша: {key}")
            return data["value"]
        return None

    def set(self, key: str, value, ttl: int = 3600):
        self._cache[key] = {
            "value": value,
            "expire": datetime.now() + timedelta(seconds=ttl)
        }
        logger.info(f"Данные сохранены в кеш: {key} (TTL: {ttl}s)")


cache = Cache()