from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route, WebSocketRoute

from core import init_core_modules
from core.lib import util, logger
from core.settings import settings

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
LOGGER.info('launch fastapi application with cfg: %s' % util.pfmt(FASTAPI_CFG))

# 加载核心模块
init_core_modules(APP)

# 加载业务模块
from .handler import test as test_handler
APP.include_router(test_handler.ROUTER)

# 打印已加载的路由
LOGGER.info('routers are:')
for route in APP.routes:
    if isinstance(route, Route):
        LOGGER.info('http router %s: %s %s' %
                    (route.name, route.path, route.methods))
    elif isinstance(route, WebSocketRoute):
        LOGGER.info('websocket router %s: %s ' %
                    (route.name, route.path))

# 加载中间件
APP.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)
LOGGER.info('middlewares are:')
for middleware in APP.user_middleware:
    LOGGER.info(repr(middleware))


from app.service import test
test.init_market()

