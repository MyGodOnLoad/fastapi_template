import asyncio
import time

from fastapi import APIRouter

from core.lib import logger

ROUTER = APIRouter()

LOGGER = logger.for_handler('demo')


@ROUTER.get('/test1')
def test1():
    time.sleep(2)
    LOGGER.info('test1')
    return


@ROUTER.get('/test2')
async def test2():
    await asyncio.sleep(3)
    LOGGER.info('test2')
    return


@ROUTER.get('/test3')
async def test3():
    time.sleep(2)
    LOGGER.info('test3')
    return
