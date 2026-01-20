import os
from celery import Celery
from kombu import Queue

broker_url = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")
backend_url = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery("board_app", broker=broker_url, backend=backend_url, include=["tasks.process"])
celery_app.conf.task_queues = (Queue("default"), Queue("activity"))
celery_app.conf.task_routes = {
    "tasks.activity.*": {
        "queue": "activity"
    }
}