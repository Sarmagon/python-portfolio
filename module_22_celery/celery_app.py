from celery import Celery
from celery.schedules import crontab

# Создаём экземпляр Celery приложения
celery_app = Celery(
    'image_service',
    broker='redis://127.0.0.1:6379/0',
    backend='redis://127.0.0.1:6379/1',
)

# Основные настройки Celery
celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Europe/Moscow',
    enable_utc=True,
    # Расписание периодических задач (Celery Beat)
    beat_schedule={
        'weekly-newsletter': {
            'task': 'tasks.send_weekly_newsletter',
            'schedule': crontab(day_of_week='monday', hour=9, minute=0),
        },
    }
)

# Импорт задач в конце, чтобы Celery их увидел
import tasks