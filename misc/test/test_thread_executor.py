import os
import time

from core.lib.cfg import get_root_path
from core.lib.thread_executor import thread_task

root_path = get_root_path()
file_path = os.path.join(root_path, 'misc', 'test', 'test.txt')


def func(param1, param2, param3):
    time.sleep(3)
    with open(file_path, 'w') as f:
        f.write(str([param1, param2, param3]))


if __name__ == '__main__':
    # func(1,3,1)
    thread_task(1, func, [1], [7], [1])

