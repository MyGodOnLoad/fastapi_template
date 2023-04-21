from celery import Celery
from kombu import Queue, Exchange

from core.lib.cfg import load_env

load_env()

from core.settings import settings

RABBITMQ_HOST = settings.RABBITMQ_HOST
RABBITMQ_PORT = settings.RABBITMQ_PORT
RABBITMQ_USERNAME = settings.RABBITMQ_USERNAME
RABBITMQ_PASSWORD = settings.RABBITMQ_PASSWORD
RABBITMQ_VHOST = settings.RABBITMQ_VHOST

celery_app = Celery(
    'celery_app',
    broker=f'amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}',
    backend=f'rpc://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}',
    include=[
        'celery_server.task_level_1',
        'celery_server.task_level_2',
    ]
)

celery_app.autodiscover_tasks()
CELERY_ROUTES = {
    'celery_server.task_level_1.*': {"queue": "task_level_1"},
    'celery_server.task_level_2.*': {"queue": "task_level_2"},
}
celery_app.conf.task_routes = CELERY_ROUTES
celery_app.conf.result_expires = 3600  # 任务结果保存时间
celery_app.conf.task_acks_late = True  # 启用延迟确认
celery_app.conf.worker_prefetch_multiplier = 1

celery_app.conf.task_track_started = True  # worker执行时标记为‘已启动’
celery_app.conf.task_always_eager = bool(settings.UNIT_TEST == "True")
