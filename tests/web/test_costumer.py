from typing import Awaitable, Callable
from unittest import IsolatedAsyncioTestCase
from aiohttp import ClientResponse

from aiohttp.test_utils import TestClient, TestServer, AioHTTPTestCase
from aiohttp.web import Application
from cache.cache_util import CacheUtil
from tests.cache.mock_dbutil import MockArea, random_str

from web.costumer import routes

ASSERT_RESP = Callable[[TestClient], Awaitable[None]]


class TestCostumerUnit(IsolatedAsyncioTestCase):
    """
    TODO: cannot set mock db_util to mocked client.
    mocked client seems in another instance.
    """

    @classmethod
    def setUpClass(cls) -> None:
        app = Application()
        app.add_routes(routes)
        cls.app = app

    async def client(self, op: ASSERT_RESP):
        async with TestClient(TestServer(self.app)) as client:
            await op(client)

    async def assertListEquals(self, expected: list, actual: list):
        if not expected and not actual:
            return
        if len(expected) != len(actual):
            self.fail(f'expected {len(expected)} items, got {len(actual)}')
        for item in actual:
            if item not in expected:
                self.fail(f'item {item} in actual but not in expected')

    async def test_get_areas(self):
        def mock_area():
            fa = MockArea()
            fa.name = random_str()
            fa.rid = random_str()
            fa.objectId = random_str()
            return fa

        async def assert_resp(client: TestClient):
            resp = await client.get('/list/areas')
            self.assertEquals(resp.status, 200)
            content = await resp.json()
            self.assertEquals(content['code'], 0)
            data = content['data']
            expected = [{'id': area.objectId, 'name': area.name}
                        for area in areas]
            self.assertListEquals(expected, data)
        LEN = 5
        util = CacheUtil()
        areas = [mock_area() for _ in range(LEN)]
        for area in areas:
            util.cache.cache_areas[area.objectId] = {'origin': area}
        await self.client(assert_resp)

    async def test_get_provinces(self):
        pass

    async def test_get_ports(self):
        pass

    async def test_get_area(self):
        pass

    async def test_get_province(self):
        pass

    async def test_get_port(self):
        pass


class TestCostumer(AioHTTPTestCase, IsolatedAsyncioTestCase):
    async def get_application(self):
        app = Application()
        app.add_routes(routes)
        return app

    async def assertSuccess(self, response: ClientResponse):
        self.assertEquals(response.status, 200)
        content = await response.json()
        self.assertEquals(content['code'], 0)
        return content['data']

    async def test_get_areas(self):
        async with self.client.request('GET', '/list/areas') as response:
            data = await self.assertSuccess(response)
            print(data)
