import os
import time

from celery import Celery

# celery = Celery(__name__)

# #redis://:password@hostname:port/db_number
# celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://:eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81@redis:6379/0")
# celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://:eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81@redis:6379/0")

celery = Celery(
    'tasks',
    backend="redis://celery-redis:6379/0",
    broker="redis://celery-redis:6379/0",
)

@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True
