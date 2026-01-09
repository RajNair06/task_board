from celery import Celery
from kombu import Queue
celery_app=Celery("board_app",broker="amqp://guest:guest@localhost:5672//",backend="redis://localhost:6379/0",include=["tasks.process"],)
celery_app.conf.task_queues=(Queue("default"),Queue("activity"))
celery_app.conf.task_routes={
    "tasks.activity.*":{
        "queue":"activity"
    }
}