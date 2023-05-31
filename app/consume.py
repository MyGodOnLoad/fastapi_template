import importlib
import inspect
from threading import Thread

from funboost import IdeAutoCompleteHelper


def load_task_functions(module_name):
    module = importlib.import_module(module_name)
    for name, func in inspect.getmembers(module, inspect.isfunction):
        if name.startswith('task_') and (
                hasattr(func, 'is_decorated_as_consume_function') and func.is_decorated_as_consume_function):
            IdeAutoCompleteHelper(func).consume()


def register_task(modules):
    for module in modules:
        Thread(target=load_task_functions, args=(module,)).start()
