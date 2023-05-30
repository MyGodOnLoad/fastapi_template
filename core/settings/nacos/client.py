import json
import os
import signal
import time
from threading import Thread

import nacos
import yaml

from core.lib import util, logger
from core.settings.settings import ContentType


LOGGER = logger.get('Nacos')


class NacosClient(object):
    def __init__(self, host, port, username, password, namespace, group, data_id, content_type):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.namespace = namespace
        self.group = group
        self.data_id = data_id
        self.content_type = content_type
        self.address = f"http://{self.host}:{self.port}"
        self.client = nacos.NacosClient(self.address, namespace=self.namespace, username=self.username, password=self.password)
        self._config = None
        self.watcher_list = []
        self.listener()

    def add_watchers(self, watchers: list):
        if not isinstance(watchers, list):
            raise
        LOGGER.debug(f"添加观察者: {watchers}")
        self.watcher_list += watchers

    def add_config_watchers(self, watchers: list):
        """
        方法会在内部使用threading.Lock对象来进行同步
        而Lock对象是不能被序列化的，因此在多进程中使用add_config_watchers方法时会报错cannot pickle '_thread.RLock' object。
        """
        self.client.add_config_watchers(self.data_id, self.group, watchers)

    def get_config(self):
        data = self.client.get_config(self.data_id, self.group)
        config = self.parser_config(data)
        return config

    def parser_config(self, content):
        """解析nacos数据"""
        if self.content_type == ContentType.yaml:
            config = yaml.safe_load(content)
        elif self.content_type == ContentType.json:
            config = json.loads(content)
        else:
            config = content
        return config

    def refresh_settings(self, config):
        """刷新配置"""
        content = config.get('content')
        config = self.parser_config(content)
        print('从nacos读取配置发生变更: %s' % util.pfmt(config))
        # 配置变更后重启，可以使用supervisor进行进程管理
        # 如果采用k8s部署，可以杀死服务，由k8s删除并新建服务pod
        # 获取进程ID
        pid = os.getpid()
        # 向进程发送SIGTERM信号
        os.kill(pid, signal.SIGTERM)

    def reset_config(self):
        self._config = None

    def listener(self):
        def _f():
            while True:
                if self.watcher_list:
                    config = self.get_config()
                    if self._config is None:
                        self._config = config
                    if not dict_equal(self._config, config):
                        for watcher in self.watcher_list:
                            LOGGER.debug(f"触发观察者：{watcher}")
                            watcher(config)

                time.sleep(3)

        Thread(target=_f, daemon=True).start()


def dict_equal(dict1, dict2):
    return json.dumps(dict1, sort_keys=True) == json.dumps(dict2, sort_keys=True)
