from core.settings import settings
from core.lib.rabbit import RabbitTool


def push_tech_results(result):
    rabbitmq = settings.rabbitmq
    rabbit_app = RabbitTool(
        rabbitmq.host,
        rabbitmq.port,
        rabbitmq.username,
        rabbitmq.password,
        rabbitmq.vhost,
    )
    exchange_name = 'test'
    queue_name = 'test_result'
    rabbit_app.exchange_declare(exchange_name)
    rabbit_app.queue_declare(queue_name)
    rabbit_app.queue_bind(queue_name, exchange_name)
    rabbit_app.publish(exchange_name, queue_name, result)
    rabbit_app.close()
