from celery import Celery
from kombu import Queue
celery_app=Celery("board_app",broker="amqp://guest:guest@localhost:5672//",backend="redis://localhost:6379/0",include=["tasks.log"],)
celery_app.conf.task_queues=(Queue("default"),Queue("audit"),)
celery_app.conf.task_routes={
    "tasks.audit.*":{
        "queue":"audit"
    }
}