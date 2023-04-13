from concurrent.futures.thread import ThreadPoolExecutor


def thread_task(workers_num, task, *args, **kwargs):
    """
    线程执行任务
    task: 任务函数
    num：线程数量
    Returns
    -------

    """
    executor = ThreadPoolExecutor(max_workers=workers_num)
    executor.map(task, *args, **kwargs)
    executor.shutdown(wait=False)  # 非阻塞
