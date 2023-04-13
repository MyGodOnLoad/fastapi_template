import socket
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.scheduler.tasks import remove_temp_file
from core.lib import logger

LOGGER = logger.for_service('scheduler')

Config = {
    # 配置存储器
    # "jobstores":{
    #     # 使用redis存储
    #     "default": RedisJobStore(redis_config)
    # },
    # 配置执行器
    # "executors": {
    #     # 默认使用线程池调度
    #     # 使用进程池调度，设置最大进程数
    #     "default": ProcessPoolExecutor(3)
    # },
    # 创建job时的默认参数
    # "job_defaults": {
    #     "coalesce": True,  # 是否并行执行
    #     "max_instances": 1  # 最大实例数
    # }
}


def register_scheduler(app):
    try:
        # 绑定端口，防止多worker重复启动
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 18000))
    except Exception as e:
        LOGGER.info('已启动一个任务计划进程')
    else:
        app.scheduler = AsyncIOScheduler(**Config)
        app.scheduler.add_job(remove_temp_file, 'cron', hour=23, misfire_grace_time=300)
        app.scheduler.start()


if __name__ == '__main__':
    # scheduler = BackgroundScheduler()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(remove_temp_file, 'cron', hour=14, minute=35)
    scheduler.start()

    while True:
        print('----')
        time.sleep(3)
