from celery import shared_task

from celery_server.decorator import celery_task, celery_task_lazy


@shared_task()
def test_task2(x: int, y: int) -> int:
    return x + y


# @celery_task(celery_app)
@celery_task_lazy()
def test_task4(words):
    print(f'{words = }')
    return 'task4'


@shared_task()
def test_task6(words):
    print(f'{words = }')
    print(type(words))  # <class 'dict'>
    return words
