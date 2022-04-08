from datetime import datetime
from unittest import TestCase
from db.basedbutil import IDT

from tests.util.mock_dbutil import MockBaseClazz, MockDbUtil

from util.cache import BaseClazzEncoder, CacheDB


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


class TestCacheDB(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cachedb = CacheDB(db_util=MockDbUtil())
        cls.dbutil = MockDbUtil()

    def test_refresh_areas(self):
        self.cachedb.refresh_areas()
        self.assertDictEqual(self.cachedb.cache_provinces, {})
        self.assertDictEqual(self.cachedb.cache_ports, {})
        ids = list({a.objectId for a in self.dbutil.get_areas()})
        cids = list({a['objectId'] for a in self.cachedb.cache_areas.values()})
        self.assertListEqual(ids, cids)

    def test_refresh_provinces(self):
        ID=self.dbutil.get_areas()[0].objectId
        self.cachedb.refresh_provinces(ID)
        provinces = self.dbutil.get_provinces(ID,IDT.ID)
        ids = [p.objectId for p in provinces]


    def test_refresh_provinces_all(self):
        pass

    def test_refresh_provinces_unexist(self):
        pass
