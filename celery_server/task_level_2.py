from celery_server.celery import celery_app


@celery_app.task()
def test_task2(x: int, y: int) -> int:
    return x + y
