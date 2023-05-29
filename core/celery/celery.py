import os
import sys
import threading
from multiprocessing import Process

from celery import Celery

from core.lib.logger import get

logger = get("celery")


def celery_init():
    from core.celery import celeryconfig
    from core.settings import settings

    CELERY_NAME = settings.CELERY_NAME
    celery_app = Celery(CELERY_NAME)
    celery_app.config_from_object(celeryconfig)
    celery_app.autodiscover_tasks(packages=['celery_server'])
    return celery_app


def register_celery(app):
    app.state.celery_app = celery_init()


def start_flower(app, port=5555):
    celery_app = getattr(app.state, 'celery_app')
    if celery_app is None:
        raise Exception("未注册celery")

    def _f():
        python_executable = sys.executable
        cmd = f'''{python_executable} -m celery  --broker={celery_app.conf.broker_url}  
        --result-backend={celery_app.conf.result_backend}   
        flower --address=0.0.0.0 --port={port}  --auto_refresh=True '''

        logger.info(f'启动flower命令:   {cmd}')
        os.system(cmd)

    threading.Thread(target=_f).start()


def start_celery_worker(app, queue_name, pool, concurrency, max_tasks_per_child):
    celery_app = getattr(app.state, 'celery_app')
    if celery_app is None:
        raise Exception("未注册celery")

    def _f():
        argv = ['worker', f'--pool={pool}', f'--concurrency={concurrency}',
                '-n', f'{queue_name}@%h', f'--loglevel=INFO',
                f'--queues={queue_name}', f'--max-tasks-per-child={max_tasks_per_child}',
                ]
        logger.info(f'celery 启动work参数 {argv}')
        celery_app.worker_main(argv)

    threading.Thread(target=_f).start()
