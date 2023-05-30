import json
import os
import signal

import yaml

from core.lib import util
from core.settings.settings import ContentType


def parser_config(config, content_type):
    """解析nacos数据"""
    content = config.get('content')
    if content_type == ContentType.yaml:
        config = yaml.safe_load(content)
    elif content_type == ContentType.json:
        config = json.loads(content)
    return config


def refresh_settings(config):
    """刷新配置"""
    from core.settings import nacos_settings
    config = parser_config(config, nacos_settings.content_type)
    print('从nacos读取配置发生变更: %s' % util.pfmt(config))
    # 配置变更后重启，可以使用supervisor进行进程管理
    # 如果采用k8s部署，可以杀死服务，由k8s删除并新建服务pod
    # 获取进程ID
    pid = os.getpid()
    # 向进程发送SIGTERM信号
    os.kill(pid, signal.SIGTERM)


def watcher1(config):
    print("Watcher1")
