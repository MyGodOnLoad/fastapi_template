import json
import os
import signal

import nacos
import yaml

from core.lib import util
from core.settings.settings import ContentType


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
        self.watcher_list = [self.refresh_settings]

    def add_watchers(self, watchers):
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
