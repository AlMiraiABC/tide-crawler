import random
from unittest import TestCase

from db.common import ExecState
from db.leancloud.lc_model import LCArea, LCPort, LCProvince, LCTide
from db.leancloud.lc_util import LCUtil

import leancloud


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
    port.province = province
    port.zone = random_str()
    port.raw = random_str()
    port.name = random_str()
    port.rid = random_str()
    port.geopoint = leancloud.GeoPoint(0, 0)
    if save:
        port.save()
    return port


class TestLCUtilInit(TestCase):
    def test_init(self):
        lc = LCUtil()
        print(lc)
        self.assertIsNotNone(lc)

    def test_logout(self):
        lc = LCUtil()
        lc.logout()
        cu = leancloud.User.get_current()
        self.assertIsNone(cu)


class TestLCUtilAdd(TestCase):
    lc: LCUtil = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.lc = LCUtil()
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.lc.logout()
        return super().tearDownClass()

    def test_close_closed(self):
        """logout when has been logged out."""
        self.lc.logout()

    def test_try_insert(self):
        # TODO Forbidden writing by object's ACL
        """insert objects successfully."""
        def save(o):
            o = LCArea()
            o.raw = area.raw
            o.name = area.name
            o.rid = area.rid
            return o

        area = add_area(False)
        (ret, inserted) = self.lc.try_insert(area, 'rid', save, LCArea)
        self.assertEquals(ret, ExecState.CREATE)
        self.assertTrue(inserted.is_existed())
        delete(inserted)

    def test_try_insert_update(self):
        # TODO Forbidden writing by object's ACL
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
        (ret, updated) = self.lc.try_insert(arean, 'rid', save, LCArea)
        self.assertEquals(ret, ExecState.UPDATE)
        self.assertEquals(updated.objectId, area.id)
        self.assertEquals(updated.name, arean.name)
        delete(updated)

    def test_add_area_id_unexist(self):
        """add_area compared by id and unexist so create it."""
        area = add_area(False)
        (ret, _) = self.lc.add_area(area, 'id')
        self.assertEquals(ret, ExecState.CREATE)
        delete(area)

    def test_add_area_id_exist(self):
        """add_area compared by id and exist so update it."""
        area = add_area()
        id = area.id  # get new id
        area = LCArea.create_without_data(id)
        area.raw = random_str()
        area.name = random_str()
        area.rid = random_str()
        (ret, updated) = self.lc.add_area(area, 'id')
        self.assertEquals(ret, ExecState.UPDATE)
        self.assertEquals(updated.name, area.name)
        delete(updated)

    def test_add_area_rid_unexist(self):
        """add_area compared by rid and unexist so create it."""
        area = add_area(False)
        (ret, inserted) = self.lc.add_area(area, 'rid')
        self.assertEquals(ret, ExecState.CREATE)
        self.assertEquals(inserted.rid, area.rid)
        delete(inserted)

    def test_add_area_rid_exist(self):
        """add_area compared by rid but unexist so update it."""
        area = add_area()
        arean = LCArea()
        arean.raw = random_str()
        arean.name = random_str()
        arean.rid = area.rid
        (ret, updated) = self.lc.add_area(arean, 'rid')
        self.assertEquals(ret, ExecState.UPDATE)
        self.assertEquals(updated.name, arean.name)
        delete(updated)

    def test_add_province_area_exist(self):
        """add_province by id """
        area = add_area()
        a = LCArea.create_without_data(area.id)
        province = add_province(a, False)
        (ret, inserted) = self.lc.add_province(province, 'id')
        self.assertEquals(ret, ExecState.CREATE)
        self.assertEquals(inserted.area.id, area.id)
        delete(inserted, area)

    def test_add_province_area_unexist(self):
        """add_province failed and raise exception becase area doesn't exist."""
        area = add_area(False)
        province = add_province(area, False)
        with self.assertRaises(ValueError):
            self.lc.add_province(province, 'id')

    def test_add_province_area_rid_exist(self):
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
        (ret, inserted) = self.lc.add_province(province, 'rid')
        self.assertEquals(ret, ExecState.CREATE)
        self.assertEquals(inserted.area.id, area.id)
        delete(inserted, area)

    def test_add_port_geo_geopoint(self):
        """
        add_port successfully with a GeoPoint type
        """
        area = add_area()
        province = add_province(area)
        port = LCPort()
        port.raw = random_str()
        port.rid = random_str()
        port.province = province
        port.zone = random_str()
        port.geopoint = leancloud.GeoPoint(0, 0)
        (ret, inserted) = self.lc.add_port(port, 'id')
        self.assertEquals(ret, ExecState.CREATE)
        delete(inserted, port, area)

    def test_add_port_geo_tuple(self):
        """
        add_port successfully with a GeoPoint type
        """
        area = add_area()
        province = add_province(area)
        port = LCPort()
        port.raw = random_str()
        port.rid = random_str()
        port.province = province
        port.zone = random_str()
        port.geopoint = (0, 0)
        (ret, inserted) = self.lc.add_port(port, 'id')
        self.assertEquals(ret, ExecState.CREATE)
        delete(inserted, port, area)


class TestLCUtilGet(TestCase):
    lc: LCUtil = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.lc = LCUtil()
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.lc.logout()
        return super().tearDownClass()
