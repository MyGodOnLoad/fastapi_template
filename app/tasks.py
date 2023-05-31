import time
from functools import wraps
from threading import Thread

from funboost import boost, BrokerEnum, IdeAutoCompleteHelper

task_list = list()


def register_task():
    def _f():
        global task_list
        while True:
            if task_list:
                task = task_list.pop()
                """
                ? 在以多进程启动的服务中，不能使用multi_process_consume方法再次fork多进程
                """
                IdeAutoCompleteHelper(task).consume()
            time.sleep(3)

    Thread(target=_f).start()


def add_task(func):
    global task_list
    task_list.append(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


# @add_task
@boost('queue_add', is_using_rpc_mode=True, broker_kind=BrokerEnum.MEMORY_QUEUE, concurrent_num=3)
def task_add(x, y):
    print(f'{x + y =}')
    return x + y


def task_delete(pk):
    return pk
