import functools
import json

from celery import shared_task

from core.lib.compress import compressor
from core.lib.time_it import time_it


def celery_task(app, *args, **kwargs):

    def decorator(f):

        @app.task(*args, **kwargs)
        @time_it
        @functools.wraps(f)
        def wapper(params):
            data = compressor.decompress_base64(params)
            _params = json.loads(data)
            result = f(**_params)
            result = compressor.compress_base64(json.dumps(result))
            return result

        return wapper
    return decorator


def celery_task_lazy(*args, **kwargs):

    def decorator(f):

        @shared_task(*args, **kwargs)
        @time_it
        @functools.wraps(f)
        def wapper(params):
            data = compressor.decompress_base64(params)
            _params = json.loads(data)
            result = f(**_params)
            result = compressor.compress_base64(json.dumps(result))
            return result

        return wapper
    return decorator
