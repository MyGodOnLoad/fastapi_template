import heapq

from core.lib import util
from core.lib.cfg import load_env
from core.settings.nacos.client import NacosClient
from core.settings.settings import Settings, NacosSettings
from core.settings.watchers import refresh_settings, watcher1, watcher2

settings: Settings
nacos_settings: NacosSettings

# 优先加载本地配置文件
load_env()


class MultiSettings(object):

    def __init__(self):
        self._heap = []

    def register_settings(self, index: int, s):
        # 数字越大，优先级越高
        heapq.heappush(self._heap, (index, s))

    def list_settings(self):
        return self._heap

    def get_configs(self):
        configs = {}
        # 优先使用本地配置
        for _, s in self._heap:
            config = s.get_config()
            self.update_config(configs, config)
        return configs

    def update_config(self, config_1, config_2):
        for k, v in config_2.items():

            if isinstance(v, dict):
                if not config_1.get(k):
                    config_1[k] = {}
                self.update_config(config_1[k], config_2[k])
            elif v is not None:
                config_1[k] = v

    def get_settings(self):
        configs = self.get_configs()
        return Settings(**configs)


def load_config():
    global settings, nacos_settings

    ms = MultiSettings()

    nacos_settings = NacosSettings()
    if nacos_settings.host:
        nc_settings = NacosClient(**nacos_settings.dict())
        # ! 多进程报错：cannot pickle '_thread.RLock' object
        # nc_settings.add_config_watchers([watcher1, refresh_settings])
        nc_settings.add_watchers([watcher1, watcher2])
        ms.register_settings(1, nc_settings)  # 数字越大，优先级越高

    local_settings = Settings()
    ms.register_settings(2, local_settings)

    settings = ms.get_settings()
    print('setting配置: %s' % util.pfmt(settings.dict(), width=120))


load_config()
