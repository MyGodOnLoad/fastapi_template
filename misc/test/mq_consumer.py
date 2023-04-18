from core.lib.rabbit import RabbitTool

host = 'rabbitmq'
port = 5672
username = 'guest'
pwd = 'guest'
vhost = '/'


def callback(ch, method, properties, body):
    # 定义一个回调函数，用来接收生产者发送的消息
    print("[消费者] recv %s" % body)
    # with open('result.json', 'wb') as f:
    #     f.write(body)


tool = RabbitTool(host, port, username, pwd, vhost)
tool.exchange_declare('test')
tool.queue_declare('test_result')
tool.queue_bind('test_result', 'test')
tool.consume('test_result', callback)
tool.channel.start_consuming()
