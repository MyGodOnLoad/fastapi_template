from celery_server.celery import celery_app
from celery_server.decorator import celery_task


@celery_app.task()
def test_task2(x: int, y: int) -> int:
    return x + y


@celery_task(celery_app)
def test_task4(words):
    print(f'{words = }')
    return 'task4'


@celery_app.task()
def test_task6(words):
    print(f'{words = }')
    print(type(words))  # <class 'dict'>
    return words
