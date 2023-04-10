from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str
    TITLE: str
    DESCRIPTION: str
    VERSION: str

    # 是否单元测试
    UNIT_TEST: str

    RABBITMQ_HOST: str
    RABBITMQ_PORT: str
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_VHOST: str

    class Config:
        case_sensitive = True


settings = Settings()
