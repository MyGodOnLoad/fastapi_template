from functools import wraps

import pika


class RabbitTool(object):
    """rabbitmq工具"""

    def __init__(self, host, port, username, pwd, vhost):
        self.host = host
        self.port = port
        self.username = username  # 指定远程rabbitmq的用户名密码
        self.pwd = pwd
        self.vhost = vhost
        self.exchange = None
        self.queue = None

        self.credentials = self._plain_credentials()
        self.conn_paramerter = self._conn_parameters()
        self.conn = self._connect()
        self.channel = self._create_channel()
        self.conn.process_data_events()

    def _plain_credentials(self):
        return pika.PlainCredentials(self.username, self.pwd)

    def _conn_parameters(self):
        # error: delivery acknowledgement on channel 1 timed out
        # 保持连接为长连接，关闭RabbitMQ的心跳检测机制
        return pika.ConnectionParameters(
            host=self.host, port=self.port, virtual_host=self.vhost,
            credentials=self.credentials, heartbeat=0)

    def _connect(self):
        """创建连接"""
        return pika.BlockingConnection(self.conn_paramerter)
        # return pika.SelectConnection(self.conn_paramerter)

    def _create_channel(self):
        """在连接上创建一个通道，通道号默认"""
        return self.conn.channel()

    def _reconnect(self):
        """重新连接"""
        print('rabbit tool 重新连接...')
        print(f'{self.exchange =}')
        print(f'{self.queue =}')
        self.conn = self._connect()
        self.channel = self._create_channel()
        self.conn.process_data_events()
        self.queue_declare(self.queue)
        if self.exchange:
            self.exchange_declare(self.exchange)
            self.queue_bind(self.queue, self.exchange)

    def close(self):
        self.conn.close()

    def _error_handler(func):
        """装饰器，连接断开后自动创建连接"""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.conn.is_closed:
                self._reconnect()
            res = func(self, *args, **kwargs)
            return res
        return wrapper

    def exchange_declare(self, exchange):
        """
        exchange声明属性
        Notes:
            如果已存在exchange的属性不能修改
        Parameters
        ----------
        exchange
            exchange名
        Returns
        -------

        """
        self.exchange = exchange
        self.channel.exchange_declare(exchange, durable=True)

    def queue_declare(self, queue):
        """
        queue声明属性
        Notes:
            如果已存在queue的属性不能修改
        Parameters
        ----------
        queue
            queue名
        Returns
        -------

        """
        self.queue = queue
        self.channel.queue_declare(queue, durable=True)

    def queue_bind(self, queue, exchange, routing_key=None):
        self.channel.queue_bind(queue, exchange, routing_key=routing_key)

    @_error_handler
    def publish(self, exchange, routing_key, message):
        """
        虽然 exchange 和 queue 都申明了持久化，但如果消息只存在内存里，
        rabbitmq 重启后，内存里的东西还是会丢失。所以必须声明消息也是持久化，从内存转存到硬盘。
        Returns
        -------

        """
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2))

    @_error_handler
    def consume(self, queue, callback, auto_ack=True):
        """
        消费者（consumer）调用callback函数时，会存在处理消息失败的风险，如果处理失败，则消息丢失。
        但是也可以选择消费者处理失败时，将消息回退给 rabbitmq ，重新再被消费者消费，这个时候需要设置确认标识。
        Returns
        -------

        """
        self.channel.basic_consume(queue, callback, auto_ack=auto_ack)
