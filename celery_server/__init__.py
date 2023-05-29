"""可以使用命令行启动"""
from app import APP


celery_app = APP.state.celery_app

celery_app.conf.task_routes = {
    'celery_server.task_level_1.*': {"queue": "task_level_1"},
    'celery_server.task_level_2.*': {"queue": "task_level_2"},
}
