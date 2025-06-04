from celery import Celery

from src.config import settings

celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,  # адрес брокера
    include=[
        "src.tasks.tasks"  # задаем путь к таскам
    ],
)

celery_instance.conf.beat_schedule = {
    "luboe_nazvanie": {
        "task": "booking_today_checkin",  # псевдоним запускаемой ф-ии из tasks.py
        "schedule": 5,  # период запусков, сек
    }
}
