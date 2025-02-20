import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class Cache:
    def __init__(self):
        self._storage = {}
        self.hits = 0
        self.misses = 0

    def get(self, key: str):
        """Получить данные из кеша"""
        data = self._storage.get(key)
        if data and data['expire'] > datetime.now():
            self.hits += 1
            logger.debug(f"Cache HIT: {key}")
            return data['value']
        self.misses += 1
        logger.debug(f"Cache MISS: {key}")
        return None

    def set(self, key: str, value, ttl: int = 3600):
        """Сохранить данные в кеш"""
        self._storage[key] = {
            'value': value,
            'expire': datetime.now() + timedelta(seconds=ttl)
        }
        logger.info(f"Кеш SET: {key} ({ttl}s)")

    def delete(self, *keys):
        """Удалить данные из кеша"""
        for key in keys:
            if key in self._storage:
                del self._storage[key]
        logger.info(f"Кеш DEL: {keys}")

    def get_stats(self):
        """Статистика использования"""
        return {"hits": self.hits, "misses": self.misses}

cache = Cache()
