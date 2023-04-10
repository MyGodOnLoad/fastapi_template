from celery_server.celery import celery_app


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"
