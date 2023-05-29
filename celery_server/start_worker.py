from app import APP
from core.celery.celery import start_flower, start_celery_worker

if __name__ == '__main__':
    start_flower(APP)
    start_celery_worker(APP, 'task_level_1', 'threads', 5, 100)
    start_celery_worker(APP, 'task_level_2', 'threads', 5, 100)
