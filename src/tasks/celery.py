from celery import Celery


TASKS_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'

celery = Celery("tasks", broker=TASKS_BROKER_URL, backend="rpc://", include=["src.tasks.tasks"])
