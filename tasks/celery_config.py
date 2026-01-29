import os
from celery import Celery
from kombu import Queue

broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
backend_url = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

celery_app = Celery("board_app", broker=broker_url, backend=backend_url, include=["tasks.process"])
celery_app.conf.task_queues = (Queue("default"), Queue("activity"))
celery_app.conf.task_routes = {
    "tasks.activity.*": {
        "queue": "activity"
    }
}
celery_app.conf.broker_connection_retry_on_startup = True
