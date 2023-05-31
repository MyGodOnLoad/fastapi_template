from fastapi import FastAPI
from starlette.routing import Route, WebSocketRoute

from core import init_core_modules
from core.celery.celery import register_celery
from core.lib import util, logger
from core.settings import settings
from .consume import register_task
from .exception import register_exceptions
from .handler import register_router
from .middleware import register_middlewares
from .scheduler.scheduler import register_scheduler
# from .tasks import register_task

LOGGER = logger.get('FASTAPI_APP')


"""
FastAPI application main module
The APP instance will be launched by uvicorn instance in ${workspaceFolder}/main.py
"""
FASTAPI_CFG = {
    'env': settings.ENV,
    'title': settings.TITLE,
    'description': settings.DESCRIPTION,
    'version': settings.VERSION,
}
APP = FastAPI(**FASTAPI_CFG)
LOGGER.info(f'launch fastapi application with cfg: {util.pfmt(FASTAPI_CFG)}')

# 加载核心模块
init_core_modules(APP)
# 注册自定义错误
register_exceptions(APP)
# 注册中间件
register_middlewares(APP)
LOGGER.info('middlewares are:')
for middleware in APP.user_middleware:
    LOGGER.info(repr(middleware))

# 注册业务路由
register_router(APP)
# 注册celery
register_celery(APP)
# 注册定时任务
register_scheduler(APP)
# 注册消费者，指定任务函数所在模块，任务函数必须以task_开头
register_task(['app.tasks'])

# 打印已加载的路由
LOGGER.info('routers are:')
for route in APP.routes:
    if isinstance(route, Route):
        LOGGER.info('http router %s: %s %s' %
                    (route.name, route.path, route.methods))
    elif isinstance(route, WebSocketRoute):
        LOGGER.info('websocket router %s: %s ' %
                    (route.name, route.path))

from app.service import test
test.init_market()
