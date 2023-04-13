from core.settings import settings
from tools.rabbit import RabbitTool


def push_tech_results(result):
    rabbit_app = RabbitTool(
        settings.RABBITMQ_HOST,
        settings.RABBITMQ_PORT,
        settings.RABBITMQ_USERNAME,
        settings.RABBITMQ_PASSWORD,
        settings.RABBITMQ_VHOST,
    )
    exchange_name = 'test'
    queue_name = 'test_result'
    rabbit_app.exchange_declare(exchange_name)
    rabbit_app.queue_declare(queue_name)
    rabbit_app.queue_bind(queue_name, exchange_name)
    rabbit_app.publish(exchange_name, queue_name, result)
    rabbit_app.close()
