import os
import sys
import time
import uuid

import pytest
import typing

from py.xml import html

Base_Dir = os.path.abspath(__file__).split('misc')[0]
sys.path.insert(0, Base_Dir)

from core.lib import cfg

opts = cfg.get_cmd_opts()
cfg.load_env('dev')


UUID: typing.Optional[uuid.uuid4] = None

"""-----------------------------------------------测试报告配置-----------------------------------------"""


# 编辑报告标题
def pytest_html_report_title(report):
    report.title = "自动化测试报告"


def pytest_configure(config):
    """修改Environment部分信息"""
    config._metadata["项目名称"] = "web项目冒烟用例"
    pass


def pytest_html_results_summary(prefix, summary, postfix):
    """修改Summary部分的信息"""
    prefix.extend([html.p("所属部门: 测试部")])
    pass


def pytest_collection_modifyitems(items):
    # item表示每个测试用例，解决用例名称中文显示问题
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode-escape")


# 测试结果表格
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('用例描述', class_="sortable", col="name"))
    # cells.insert(4, html.th('执行时间', class_='sortable time', col='time'))
    cells.pop()


def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    # cells.insert(4, html.td(strftime('%Y-%m-%d %H:%M:%S'), class_='col-time'))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if item.function.__doc__ is None:
        report.description = str(item.function.__name__)
    else:
        report.description = str(item.function.__doc__)
    report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")  # 设置编码显示中文


"""-----------------------------------------单元测试配置------------------------------------------"""


# 指定异步工具anyio，asyncio，trio
# @pytest.fixture
# def anyio_backend():
#     return 'asyncio'


@pytest.fixture()
def gen_uuid():
    global UUID
    if not UUID:
        UUID = uuid.uuid4()

    return str(UUID)


@pytest.fixture()
def write_redis_progress(gen_uuid):
    from core.lib.thread_executor import thread_task
    from core.lib.redis import redis_client

    def func(_):
        print("redis中开始写入进度数值")
        for i in range(101):
            time.sleep(0.5)
            redis_client.hset('progress', gen_uuid, i)

    thread_task(1, func, [1])
