from datetime import datetime
from unittest import IsolatedAsyncioTestCase, TestCase

from storages.basedbutil import IDT
from tests.cache.mock_dbutil import MockBaseClazz, MockDbUtil

from cache.cache_db import _PRE_ID, BaseClazzEncoder, CacheDB


class TestBaseClazzEncoder(TestCase):
    def test_default(self):
        OBJID = '12345678'
        D1 = datetime(2010, 12, 12)
        D2 = datetime(2020, 10, 10)
        base = MockBaseClazz()
        base.objectId = OBJID
        base.createdAt = D1
        base.updatedAt = D2
        d = BaseClazzEncoder().default(base)
        expect = {'objectId': OBJID,
                  'updatedAt': '2020-10-10T00:00:00',
                  'createdAt': '2010-12-12T00:00:00',
                  'origin': base}
        self.assertDictEqual(d, expect)


class TestCacheDB(IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dbutil = MockDbUtil()
        cls.cachedb = CacheDB(db_util=cls.dbutil)

    async def test_refresh_areas(self):
        await self.cachedb.refresh_areas()
        self.assertDictEqual(self.cachedb.cache_provinces, {})
        self.assertDictEqual(self.cachedb.cache_ports, {})
        ids = list({a.objectId for a in await self.dbutil.get_areas()})
        cids = list({a['objectId'] for a in self.cachedb.cache_areas.values()})
        self.assertListEqual(ids, cids)

    async def test_refresh_provinces(self):
        self.cachedb.cache_provinces.clear()
        await self.cachedb.refresh_areas()
        ID = (await self.dbutil.get_areas())[0].objectId
        await self.cachedb.refresh_provinces(ID)
        provinces = await self.dbutil.get_provinces(ID, IDT.ID)
        ids = list({p.objectId for p in provinces})
        cids = list(
            {p['objectId'] for p in self.cachedb.cache_areas[_PRE_ID+ID]['provinces'].values()})
        pids = list({p['objectId']
                    for p in self.cachedb.cache_provinces.values()})
        self.assertListEqual(ids, cids)
        self.assertListEqual(ids, pids)

    def test_refresh_provinces_all(self):
        pass

    def test_refresh_provinces_unexist(self):
        pass
