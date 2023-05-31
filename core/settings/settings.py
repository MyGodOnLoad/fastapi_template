from enum import Enum
from typing import Optional

from pydantic import BaseSettings, Extra


class ContentType(str, Enum):
    yaml = 'yaml'
    json = 'json'


class NacosSettings(BaseSettings):
    host: Optional[str]
    port: Optional[str]
    username: Optional[str]
    password: Optional[str]
    namespace: Optional[str]
    group: Optional[str]
    data_id: Optional[str]
    content_type: Optional[str] = ContentType.yaml

    class Config:
        env_prefix = 'NACOS_'
        extra: Extra = Extra.ignore


class CelerySettings(BaseSettings):
    name: Optional[str]

    class Config:
        env_prefix = 'CELERY_'
        extra: Extra = Extra.ignore


class RabbitMQSettings(BaseSettings):
    host: Optional[str]
    port: Optional[str]
    username: Optional[str]
    password: Optional[str]
    vhost: Optional[str]

    class Config:
        env_prefix = 'RABBITMQ_'
        extra: Extra = Extra.ignore


class Settings(BaseSettings):
    ENV: str
    TITLE: str
    DESCRIPTION: str
    VERSION: str
    # 是否单元测试
    UNIT_TEST: str = 'False'

    nacos: NacosSettings = NacosSettings()

    celery: CelerySettings = CelerySettings()

    rabbitmq: RabbitMQSettings = RabbitMQSettings()

    class Config:
        case_sensitive = True  # 大小写敏感
        extra: Extra = Extra.ignore

    def get_config(self):
        return self.dict()
