import json
import time

from celery import shared_task

from celery_server.task_level_2 import test_task2, test_task4, test_task6
from core.lib.compress import compressor


@shared_task(rate_limit='10/m', queue='task_level_1')
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
            time.sleep(1)
        result = task.get(disable_sync_subtasks=False)
        results.append(result)
    print(results)
    return f"test task return {word}"


@shared_task()
def test_task3(word: str) -> str:
    params = {'words': 'Hello World'}
    data = compressor.compress_base64(json.dumps(params))
    task = test_task4.delay(data)

    result = task.get(disable_sync_subtasks=False)
    print(result)
    return f"test task return {word}"


@shared_task()
def test_task5(word: str) -> str:
    params = {'words': 'Hello World'}
    task = test_task6.delay(params)

    result = task.get(disable_sync_subtasks=False)
    print(result)
    print(type(result))
    return f"test task return {word}"
