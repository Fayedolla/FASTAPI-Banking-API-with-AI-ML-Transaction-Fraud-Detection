from celery import Celery
from backend.app.core.config import settings  # fixed typo: was 'settigns'

celery_app = Celery(
    "worker",
    # Advanced Message Queue Protocol (AMQP)
    broker=f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}//",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
)

celery_app.conf.update(
    # Task serialization
    task_serializer="json",
    result_serializer="json",
    accept_content=["application/json"],

    # Task execution
    task_track_started=True,
    task_time_limit=5 * 60,          # hard limit: 5 minutes
    task_soft_time_limit=5 * 60,     # soft limit: 5 minutes
    task_acks_late=True,             # ack only after task finishes
    task_reject_on_worker_lost=True, # requeue if worker dies

    # Retry & result settings
    result_backend_max_retries=10,
    result_backend_always_retry=True,
    result_expires=3600,             # results expire in 1 hour
    task_default_retry_delay=300,    # 5 minutes before retry
    task_max_retries=3,
    task_send_sent_event=True,
    result_extended=True,

    # Worker settings
    worker_send_task_events=True,     # fixed typo: was 'workder_send_task_events'
    worker_prefetch_multiplier=1,     # fetch 1 task at a time
    worker_max_tasks_per_child=1000,  # restart worker after 1000 tasks
    worker_max_memory_per_child=5000, # restart worker if exceeds 5000 MB

    # Queue settings
    task_default_queue="nextgen_tasks",
    task_create_missing_queues=True,

    # Logging
    worker_log_format="[%(asctime)s: %(levelname)s/%(processName)s] %(message)s",
    worker_task_log_format="[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s",
)

# Automatically discover tasks in this package
celery_app.autodiscover_tasks(
    packages=["backend.app.core.emails"],
    related_name="tasks",
    force=True,
)