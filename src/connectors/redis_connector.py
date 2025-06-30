import logging
import redis.asyncio as redis


class RedisManager:
    _redis: redis.Redis

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def connect(self):
        """Устанавливает асинхронное соединение с Redis."""
        logging.info(f"Начинаю подключение к Redis host={self.host}, port={self.port}")
        self._redis = await redis.Redis(host=self.host, port=self.port)
        logging.info(f"Успешное подключение к Redis host={self.host}, port={self.port}")

    async def set(self, key: str, value: str, expire: int | None = None):
        """Устанавливает значение в Redis с возможностью указать срок жизни (expire)"""
        if expire:
            await self._redis.set(key, value, ex=expire)
        else:
            await self._redis.set(key, value)

    async def get(self, key: str):
        """Получает значение из Redis по ключу"""
        return await self._redis.get(key)

    async def delete(self, key: str):
        """Удаляет значение из Redis по ключу"""
        await self._redis.delete(key)

    async def close(self):
        """Закрывает соединение с Redis."""
        if self._redis:
            await self._redis.close()


# Пример использования:
# redis_manager = RedisManager(redis_url="redis://localhost")
# await redis_manager.connect()
# await redis_manager.set("key", "value", expire=60)
# value = await redis_manager.get("key")
# await redis_manager.delete("key")
# await redis_manager.close()
