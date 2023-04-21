import pytest
from httpx import AsyncClient

from core.lib import cfg
from misc.test.dataset.constant import *
from app import APP

# 指定异步工具 anyio（asyncio + trio），asyncio，trio
pytestmark = pytest.mark.asyncio

root_path = cfg.get_root_path()


class TestBaseClass(object):
    relative_url = ''

    async def get(self, params=None):
        async with AsyncClient(app=APP, base_url='http://test') as client:
            resp = await client.get(self.relative_url, params=params)
        return resp

    async def post(self, params=None):
        async with AsyncClient(app=APP, base_url='http://test') as client:
            resp = await client.post(self.relative_url, json=params)
        return resp


class TestHealthCheck(TestBaseClass):
    relative_url = '/api/v1/core/health'

    async def test_case(self):
        """服务健康检测"""
        resp = await self.get()
        assert resp.status_code == 200
        assert resp.json() == {"success": True, "message": "ok", "data": None, "code": 200}

    @pytest.mark.skip
    async def test_case_1(self):
        """服务健康检测"""
        resp = await self.get()
        assert resp.status_code == 200
        assert resp.json() == {"success": True, "message": "ok", "data": None, "code": 200}


class TestCeleryAddTask(TestBaseClass):
    relative_url = 'api/v2/demo/task'

    async def test_add_task_case(self):
        """发布celery任务"""
        resp = await self.post()
        assert resp.status_code == 200
        print(resp.json())
