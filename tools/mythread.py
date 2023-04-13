import threading
import time


class ThreadTool(threading.Thread):
    """线程工具，以线程执行任务"""

    def __init__(self, func, args=()):
        super().__init__()
        self.func = func
        self.args = args
        self.result = None

    def run(self) -> None:
        start = time.time()
        self.result = self.func(*self.args)
        end = time.time()
        print(f'{self.func.__name__}耗时{end - start}s')

    def get_result(self):
        return self.result
