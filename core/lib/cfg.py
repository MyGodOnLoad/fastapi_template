import getopt
import json
import os
import sys
from typing import Any, Dict

from dotenv import load_dotenv

from core.lib import util


def get_cmd_opts() -> Dict[str, Any]:
    """
    get commandline opts
    :return: cmd options
    """
    # get options
    try:
        opts, _ = getopt.getopt(
            sys.argv[1:],
            'e:t:',
            ['env=', 'tag=']
        )
    except getopt.GetoptError as e:
        raise e
    t = {
        'env': 'dev',
        'tag': ''
    }
    for o, a in opts:
        if o == '-e':
            t['env'] = a
        elif o == '-t':
            t['tag'] = a
    return t


def load_cfg(env: str) -> Dict[str, Any]:
    """
    load configs
    :param env: app env
    :return: uvicorn cfg dict
    """
    if not env:
        raise Exception('env not specified')
    cfg_dir = os.path.join('cfg', env)
    assert os.path.isdir(cfg_dir)

    # logger cfg
    logger_cfgpath = os.path.join(cfg_dir, 'logger.json')
    logger_cfg = json.loads(open(logger_cfgpath, encoding=util.ENCODING).read())
    assert isinstance(logger_cfg, dict)

    # uvicorn cfg
    default_uvicorn_cfg = {
        'log_config': logger_cfg,
        'env_file': os.path.join(cfg_dir, 'app.cfg'),
        'loop': 'asyncio'
    }
    uvicorn_cfgpath = os.path.join(cfg_dir, 'uvicorn.json')
    uvicorn_cfg = json.loads(open(uvicorn_cfgpath, encoding=util.ENCODING).read())
    assert isinstance(uvicorn_cfg, dict)

    return dict(default_uvicorn_cfg, **uvicorn_cfg)


def get_root_path():
    """
    获取项目根目录的绝对路径
    Returns
    -------

    """
    root_path = os.path.abspath(__file__).split('core')[0]
    return root_path


def get_cfg_path(env: str) -> str:
    """
    获取指定环境的配置文件的绝对路径
    Returns
    -------

    """
    root_path = get_root_path()
    return os.path.join(root_path, 'cfg', env, 'app.cfg')


def load_env(env):
    """加载服务环境"""
    env_file = get_cfg_path(env=env)
    load_dotenv(dotenv_path=env_file)


def get(key: str, default: Any = '') -> Any:
    """
    get one config value
    :param key: config key
    :param default: default value
    :return: config value
    """
    return os.getenv(key.upper(), default)


def get_str(key: str) -> str:
    """
    get string config value
    :param key: config key
    :return: string config value
    """
    return str(get(key))


def get_bool(key: str) -> bool:
    """
    get bool config value
    :param key: config key
    :return: bool config value
    """
    return str(get(key)).upper() == 'TRUE'


def get_int(key: str, panic: bool = True) -> int:
    """
    get int config value
    :param key: config key
    :param panic: will raise exception if fail
    :return: int config vallue
    """
    try:
        return int(str(get(key)))
    except Exception as e:
        if panic:
            raise e
        print('[core.lib.cfg] get int value of key %s error' % key, file=sys.stderr)
        return 0


def get_float(key: str, panic: bool = True) -> float:
    """
    get float config  value
    :param key: config key
    :param panic: will raise exception if fail
    :return: float config value
    """
    try:
        return float(str(get(key)))
    except Exception as e:
        if panic:
            raise e
        print('[core.lib.cfg] get float value of key %s error' % key, file=sys.stderr)
        return 0.0
