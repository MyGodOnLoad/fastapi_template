import json

from tools.rabbit import RabbitTool

host = 'rabbitmq'
port = 5672
username = 'guest'
pwd = 'guest'
vhost = '/'


tool = RabbitTool(host, port, username, pwd, vhost)
tool.exchange_declare('test')
tool.queue_declare('test_result')
tool.queue_bind('test_result', 'test')
data = {
    'data': 'Hello World!',
}
tool.publish('test', 'test_result', json.dumps(data))

