"""
:Author:  HelloWorld
:Create:  2023/4/14
demo模块的api
"""
import asyncio
import time
from uuid import uuid4

from fastapi import APIRouter

from celery_server.task_level_1 import test_task1, test_task3, test_task5
from core.lib import logger
from core.lib.cprofile import do_cprofile
from core.lib.time_it import time_it
from core.model.handler import Resp

ROUTER = APIRouter()

LOGGER = logger.for_handler('demo')


@ROUTER.get('/test1')
def test1():
    """
    采用线程池的方式执行，因为它是同步函数，使用 time.sleep() 阻塞了当前线程，如果在高并发的情况下，线程池中的线程数量会被快速消耗完，导致后续请求被阻塞。
    8核  线程池 12
    """
    time.sleep(2)
    LOGGER.info('test1')


@ROUTER.get('/test2')
async def test2():
    """
    采用协程的方式执行，它使用了 async/await 语法，可以让当前协程挂起等待，不会阻塞当前线程，因此在高并发的情况下，可以更好地利用CPU资源，提高程序的并发性能。
    """
    await asyncio.sleep(3)
    LOGGER.info('test2')


@ROUTER.get('/test3')
async def test3():
    """
    在异步函数内存在同步语句
    """
    uuid = uuid4()
    print(f'start---{uuid}')
    time.sleep(2)
    print(f'middle--{uuid}')
    LOGGER.info('test3')
    print(f'end---{uuid}')


@ROUTER.get('/test4')
async def test4():
    """
    在异步函数内存在同步语句
    """
    func()
    return Resp.ok('test4')


@time_it
@do_cprofile('prof')
def func():
    time.sleep(1)


@ROUTER.post('/task')
async def add_task():
    """
    发送celery任务
    """
    tasks = []
    for i in range(3):
        task = test_task1.delay('Hello World')
        tasks.append(task)

    results = [task.get() for task in tasks]
    print(results)

    return Resp.ok('Hello World')


@ROUTER.get('/task2')
async def task2():
    """
    发送celery任务
    """
    task = test_task3.delay('Hello World')
    print(task.get())
    return Resp.ok('Hello World')


@ROUTER.get('/task3')
async def task3():
    """
    发送celery任务
    """
    task = test_task5.delay('Hello World')
    print(task.get())
    return Resp.ok('Hello World')
