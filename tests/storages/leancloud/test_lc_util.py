import asyncio
import datetime
import random
from typing import Iterable, Iterator
from unittest import IsolatedAsyncioTestCase, TestCase
from config import LCSetting

from storages.basedbutil import IDT
from storages.common import ExecState
from storages.leancloud.lc_model import (LCArea, LCBaseClazz, LCPort, LCProvince,
                                         LCTide, LCWithInfo)
from storages.leancloud.lc_util import LCUtil
from storages.model import TideItem

import leancloud

from utils.async_util import run_async


leancloud.init(LCSetting.APP_ID,
               LCSetting.APP_KEY if LCSetting.APP_KEY else LCSetting.MASTER_KEY)
leancloud.User().login(LCSetting.USERNAME, LCSetting.PASSWORD)


def delete(*args):
    """Delete :param:`args` from leancloud."""
    leancloud.Object.destroy_all(args)


def random_str(s='0123456789abcdef', l=24):
    """Generate a random string from :param:`s` with :param:`l` length."""
    return ''.join(random.choices(s, k=l))


def add_area(save: bool = True):
    area = LCArea()
    area.raw = random_str()
    area.name = random_str()
    area.rid = random_str()
    if save:
        area.save()
    return area


def add_province(area: LCArea, save: bool = True):
    province = LCProvince()
    province.area = area
    province.name = random_str()
    province.raw = random_str()
    province.rid = random_str()
    if save:
        province.save()
    return province


def add_port(province: LCProvince, save: bool = True):
    port = LCPort()
    port.name = random_str()
    port.raw = random_str()
    port.rid = random_str()
    port.province = province
    port.zone = random_str()
    port.geopoint = (0, 0)
    if save:
        port.save()
    return port


def add_tide(port: LCPort, save: bool = True):
    def ti(t: datetime.time = datetime.datetime.now().time(), h: float = random.random()*10):
        return TideItem(t, h)
    day = [ti(datetime.time(i)) for i in range(24)]
    limit = [ti(datetime.time(i)) for i in random.sample(range(24), 3)]
    tide = LCTide()
    tide.limit = limit
    tide.day = day
    tide.date = datetime.datetime.now()
    tide.port = port
    tide.datum = random.random()*random.randint(-10, 10)
    if save:
        tide.save()
    return tide, day, limit


class TestLCUtilInit(IsolatedAsyncioTestCase):
    async def test_init(self):
        lc = LCUtil()
        self.assertIsNotNone(lc)

    async def test_logout(self):
        lc = LCUtil()
        await lc.logout()


class TestLCUtilAdd(IsolatedAsyncioTestCase):
    """LCUtil.add_*"""
    lc: LCUtil = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.lc = LCUtil()
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        run_async(cls.lc.logout())
        return super().tearDownClass()

    async def test_try_insert(self):
        # FIXME Forbidden writing by object's ACL
        """insert objects successfully."""
        def save(o):
            o = LCArea()
            o.raw = area.raw
            o.name = area.name
            o.rid = area.rid
            return o

        area = add_area(False)
        (ret, inserted) = await self.lc.try_insert(area, IDT.RID, save, LCArea)
        self.assertEqual(ret, ExecState.CREATE)
        self.assertTrue(inserted.is_existed())
        delete(inserted)

    async def test_try_insert_update(self):
        # FIXME Forbidden writing by object's ACL
        """insert objects but exists, update it."""
        def save(o):
            o.raw = arean.raw
            o.name = arean.name
            o.rid = arean.rid
            return o

        area = add_area()
        arean = LCArea()
        arean.rid = area.rid
        arean.name = random_str()
        arean.raw = random_str()
        (ret, updated) = await self.lc.try_insert(arean, IDT.RID, save, LCArea)
        self.assertEqual(ret, ExecState.UPDATE)
        self.assertEqual(updated.objectId, area.objectId)
        self.assertEqual(updated.name, arean.name)
        delete(updated)

    async def test_add_area_id_unexist(self):
        """add_area compared by id and unexist so create it."""
        area = add_area(False)
        (ret, _) = await self.lc.add_area(area, IDT.ID)
        self.assertEqual(ret, ExecState.CREATE)
        delete(area)

    async def test_add_area_id_exist(self):
        """add_area compared by id and exist so update it."""
        area = add_area()
        area.raw = random_str()
        area.name = random_str()
        area.rid = random_str()
        (ret, updated) = await self.lc.add_area(area, IDT.ID)
        self.assertEqual(ret, ExecState.UPDATE)
        self.assertEqual(updated.name, area.name)
        delete(updated)

    async def test_add_area_rid_unexist(self):
        """add_area compared by rid and unexist so create it."""
        area = add_area(False)
        (ret, inserted) = await self.lc.add_area(area, IDT.RID)
        self.assertEqual(ret, ExecState.CREATE)
        self.assertEqual(inserted.rid, area.rid)
        delete(inserted)

    async def test_add_area_rid_exist(self):
        """add_area compared by rid but unexist so update it."""
        area = add_area()
        arean = LCArea()
        arean.raw = random_str()
        arean.name = random_str()
        arean.rid = area.rid
        (ret, updated) = await self.lc.add_area(arean, IDT.RID)
        self.assertEqual(ret, ExecState.UPDATE)
        self.assertEqual(updated.name, arean.name)
        delete(updated)

    async def test_add_province_area_exist(self):
        """add_province by id """
        area = add_area()
        province = add_province(area, False)
        (ret, inserted) = await self.lc.add_province(province, IDT.ID)
        self.assertEqual(ret, ExecState.CREATE)
        self.assertEqual(inserted.area.objectId, area.objectId)
        delete(inserted, area)

    async def test_add_province_area_unexist(self):
        """add_province failed and raise exception becase area doesn't exist."""
        area = add_area(False)
        province = add_province(area, False)
        with self.assertRaises(ValueError):
            await self.lc.add_province(province, IDT.ID)

    async def test_add_province_area_rid_exist(self):
        """
        add_province
        province.rid doesn't exist
        area.rid exists
        so create it.
        """
        area = add_area()
        a = LCArea()
        a.rid = area.rid
        province = add_province(a, False)
        (ret, inserted) = await self.lc.add_province(province, IDT.RID)
        self.assertEqual(ret, ExecState.CREATE)
        self.assertEqual(inserted.area.objectId, area.objectId)
        delete(inserted, area)

    async def test_add_tide_get_set_tideitem(self):
        """add_tide and verify __to_dicts when set"""
        def convert(tideitems):
            return [tideitem.__dict__ for tideitem in tideitems]
        area = add_area()
        province = add_province(area)
        port = add_port(province)
        (tide, day, limit) = add_tide(port, save=False)
        (ret, inserted) = await self.lc.add_tide(tide, IDT.ID)
        self.assertEqual(ret, ExecState.CREATE)
        self.assertListEqual(convert(day), convert(inserted.day))
        self.assertListEqual(convert(limit), convert(inserted.limit))
        delete(inserted, port, province, area)


class TestTideItem(TestCase):
    def test_to_dict(self):
        time = datetime.datetime.now().time()
        height = random.random()*10
        ti_dict = TideItem(time, height).to_dict()
        self.assertDictEqual(
            ti_dict, {TideItem.TIME: str(time), TideItem.HEIGHT: height})

    def test_to_dict_none(self):
        """TideItem's time and height is None"""
        ti_dict = TideItem(None, None).to_dict()
        self.assertDictEqual(
            ti_dict, {TideItem.TIME: None, TideItem.HEIGHT: None})

    def test_from_dict(self):
        time = datetime.datetime.now().time()
        height = random.random()*10
        ti = TideItem.from_dict(
            {TideItem.TIME: str(time), TideItem.HEIGHT: height})
        self.assertEqual(ti.time, time)
        self.assertEqual(ti.height, height)

    def test_from_dict_value_none(self):
        """dict values are none"""
        ti = TideItem.from_dict({TideItem.TIME: None, TideItem.HEIGHT: None})
        self.assertIsNone(ti.time)
        self.assertIsNone(ti.height)


class TestLCUtilGet(IsolatedAsyncioTestCase):
    """LCUtil.get_* which return one object."""
    lc: LCUtil = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.lc = LCUtil()
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        run_async(cls.lc.logout())
        return super().tearDownClass()

    def _assert_base(self, a: LCBaseClazz, b: LCBaseClazz):
        self.assertEqual(a.objectId, b.objectId)
        self.assertEqual(a.raw, b.raw)

    def _assert_with_info(self, a: LCWithInfo, b: LCWithInfo):
        self._assert_base(a, b)
        self.assertEqual(a.rid, b.rid)
        self.assertEqual(a.name, b.name)

    async def test_get_area_id(self):
        area = add_area()
        a = await self.lc.get_area(area.objectId, IDT.ID)
        self._assert_with_info(area, a)
        delete(area)

    async def test_get_area_rid(self):
        area = add_area()
        a = await self.lc.get_area(area.rid, IDT.RID)
        self._assert_with_info(area, a)
        delete(area)

    async def test_get_area_unexist(self):
        a = await self.lc.get_area('unexistarea', IDT.ID)
        self.assertIsNone(a)

    async def test_get_province_id(self):
        area = add_area()
        province = add_province(area)
        p = await self.lc.get_province(province.objectId, IDT.ID)
        self._assert_with_info(province, p)
        self._assert_with_info(area, p.area)
        delete(province, area)

    async def test_get_province_unexist(self):
        p = await self.lc.get_province('unexistprovince', IDT.ID)
        self.assertIsNone(p)

    async def test_get_province_rid(self):
        area = add_area()
        province = add_province(area)
        p = await self.lc.get_province(province.rid, IDT.RID)
        self._assert_with_info(province, p)
        self._assert_with_info(area, p.area)
        delete(province, area)

    async def test_get_port_id(self):
        area = add_area()
        province = add_province(area)
        port = add_port(province)
        p = await self.lc.get_port(port.objectId, IDT.ID)
        self._assert_with_info(port, p)
        self._assert_with_info(province, p.province)
        delete(port, province, area)

    async def test_get_port_rid(self):
        area = add_area()
        province = add_province(area)
        port = add_port(province)
        p = await self.lc.get_port(port.objectId, IDT.ID)
        self._assert_with_info(port, p)
        self._assert_with_info(province, p.province)
        delete(port, province, area)

    async def test_get_port_unexist(self):
        p = await self.lc.get_port('unexistport', IDT.ID)
        self.assertIsNone(p)

    async def test_get_tide(self):
        area = add_area()
        province = add_province(area)
        port = add_port(province)
        (tide, _, _) = add_tide(port)
        t = await self.lc.get_tide(port.objectId, tide.date.date())
        self.assertIsNotNone(t)  # may return earlier or later row
        self.assertEqual(t.port.objectId, port.objectId)
        delete(tide, port, province, area)

    async def test_get_tide_unexist(self):
        t = await self.lc.get_tide('unexistport', datetime.datetime.now().date())
        self.assertIsNone(t)


class TestLCUtilGetList(IsolatedAsyncioTestCase):
    """LCUtil.get_* which return a list."""
    lc: LCUtil = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.lc = LCUtil()
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.lc.logout()
        return super().tearDownClass()

    def assertSubset(self, a: Iterable, b: Iterable):
        """self.assertTrue(a.issubset(b))"""
        seta = set(a)
        self.assertTrue(seta.issubset(b))

    def _id_sets(self, objects: Iterator[LCBaseClazz]) -> set:
        return {i.objectId for i in objects}

    async def test_get_areas(self):
        areas1 = [add_area() for _ in range(2)]
        areas2 = await self.lc.get_areas()
        self.assertSubset(self._id_sets(areas1), self._id_sets(areas2))
        delete(*areas1)

    async def test_get_provinces_area(self):
        """get provinces by Area instance."""
        area = add_area()
        provinces1 = [add_province(area) for _ in range(2)]
        provinces2 = await self.lc.get_provinces(area)
        self.assertSetEqual(self._id_sets(provinces1),
                            self._id_sets(provinces2))
        delete(*provinces1, area)

    async def test_get_provinces_str_id(self):
        area = add_area()
        provinces1 = [add_province(area) for _ in range(2)]
        provinces2 = await self.lc.get_provinces(area.objectId, IDT.ID)
        self.assertSetEqual(self._id_sets(provinces1),
                            self._id_sets(provinces2))
        delete(*provinces1, area)

    async def test_get_provinces_str_rid(self):
        area = add_area()
        provinces1 = [add_province(area) for _ in range(2)]
        provinces2 = await self.lc.get_provinces(area.rid, IDT.RID)
        self.assertSetEqual(self._id_sets(provinces1),
                            self._id_sets(provinces2))
        delete(*provinces1, area)

    async def test_get_provinces_unexist(self):
        provinces = await self.lc.get_provinces('unexistarea', IDT.ID)
        self.assertListEqual(provinces, [])

    async def test_get_ports_province(self):
        """get ports by Province instance"""
        area = add_area()
        province = add_province(area)
        ports1 = [add_port(province) for _ in range(2)]
        ports2 = await self.lc.get_ports(province)
        self.assertSetEqual(self._id_sets(ports1), self._id_sets(ports2))
        delete(*ports1, province, area)

    async def test_get_ports_str_id(self):
        area = add_area()
        province = add_province(area)
        ports1 = [add_port(province) for _ in range(2)]
        ports2 = await self.lc.get_ports(province.objectId, IDT.ID)
        self.assertSetEqual(self._id_sets(ports1), self._id_sets(ports2))
        delete(*ports1, province, area)

    async def test_get_ports_str_rid(self):
        area = add_area()
        province = add_province(area)
        ports1 = [add_port(province) for _ in range(2)]
        ports2 = await self.lc.get_ports(province.rid, IDT.RID)
        self.assertSetEqual(self._id_sets(ports1), self._id_sets(ports2))
        delete(*ports1, province, area)

    async def test_get_ports_unexist(self):
        ports = await self.lc.get_ports('unexistprovince', IDT.ID)
        self.assertListEqual(ports, [])
