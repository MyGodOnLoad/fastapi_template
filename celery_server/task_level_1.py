import time

from celery_server.celery import celery_app
from celery_server.task_level_2 import test_task2


@celery_app.task(rate_limit='10/m')
def test_task1(word: str) -> str:
    tasks = []
    for i in range(10):
        task = test_task2.delay(i, i)
        tasks.append(task)

    # results = [task.get(disable_sync_subtasks=False) for task in tasks]
    results = []
    for task in tasks:
        while not task.ready():
            print(task.status)
            time.sleep(0.1)
        result = task.get(disable_sync_subtasks=False)
        results.append(result)
    print(results)
    return f"test task return {word}"
