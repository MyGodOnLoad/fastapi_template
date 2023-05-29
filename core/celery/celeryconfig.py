from kombu import Queue

from core.settings import settings

RABBITMQ_HOST = settings.RABBITMQ_HOST
RABBITMQ_PORT = settings.RABBITMQ_PORT
RABBITMQ_USERNAME = settings.RABBITMQ_USERNAME
RABBITMQ_PASSWORD = settings.RABBITMQ_PASSWORD
RABBITMQ_VHOST = settings.RABBITMQ_VHOST

broker_url = f'amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}'
result_backend = f'rpc://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}'
task_track_started = True
result_serializer = "json"
accept_content = ['json']
timezone = "Asia/Shanghai"
enable_utc = True
result_expires = 60 * 60 * 24
task_acks_late = True  # 启用延迟确认
worker_prefetch_multiplier = 1  # 任务预取数量
result_compression = 'zlib'  # 指定数据传输的压缩方法,结果数据需要自行解压缩

task_always_eager = bool(settings.UNIT_TEST == "True")

# CELERY_QUEUES = (  # 设置add队列,绑定routing_key
#     Queue('default', routing_key='default'),
#     Queue('email', routing_key='send_email'),
# )
#
# CELERY_ROUTES = {
#     'app.api.api_v1.tasks.emails.decoratorEmail': {
#         'queue': 'email',
#         'routing_key': 'send_email',
#     }
# }

