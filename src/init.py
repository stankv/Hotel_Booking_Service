from connectors.redis_connector import RedisManager  # from src.connectors.redis_connector import RedisManager
from config import settings  # from src.config import settings

redis_manager = RedisManager(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)
