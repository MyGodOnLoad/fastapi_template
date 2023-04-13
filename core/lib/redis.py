import sys
from typing import Optional

from redis import Redis, ConnectionError, ResponseError

from core.lib import logger, cfg

LOGGER = logger.get('Core.Redis')


class RedisClient(object):

    def __init__(self, host: str, port: int, password: str, db: int = 0, socket_timeout: int = 5):
        self._redis_client: Optional[Redis] = None
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.socket_timeout = socket_timeout

    def init_redis_connection(self):
        """
        初始化连接
        Returns
        -------

        """
        try:
            self._redis_client = Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                socket_timeout=self.socket_timeout,
                decode_responses=True
            )
            if not self._redis_client.ping():
                LOGGER.error('连接redis超时')
                sys.exit()
        except (ConnectionError, ResponseError) as e:
            LOGGER.error(f'连接redis异常 {e}')
            LOGGER.error(f'host: {self.host}')
            LOGGER.error(f'port: {self.port}')
            LOGGER.error(f'db: {self.db}')
            LOGGER.error(f'password: {self.password}')
            sys.exit()

    def __getattr__(self, item):
        return getattr(self._redis_client, item)

    def __getitem__(self, item):
        return self._redis_client[item]

    def __setitem__(self, key, value):
        self._redis_client[key] = value

    def __delitem__(self, key):
        del self._redis_client[key]


redis_client = RedisClient(
    host=cfg.get_str('REDIS_HOST'),
    port=cfg.get_int('REDIS_PORT'),
    password=cfg.get_str('REDIS_PASSWORD'),
    db=cfg.get_int('REDIS_DB')
)

# 只允许导出 redis_client 实例化对象
__all__ = ["redis_client"]
