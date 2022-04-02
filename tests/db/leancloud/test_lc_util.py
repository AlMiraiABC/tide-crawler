import random
from unittest import TestCase

from db.common import ExecState
from db.leancloud.lc_model import LCArea
from db.leancloud.lc_util import LCUtil

import leancloud


def delete(*args):
    """Delete :param:`args` from leancloud."""
    leancloud.Object.destroy_all(args)


def random_str(s='0123456789abcdef', l=24):
    """Generate a random string from :param:`s` with :param:`l` length."""
    return ''.join(random.choices(s, k=l))


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


class TestLCUtilCRUD(TestCase):
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
        """insert objects successfully."""
        def save(o):
            o = LCArea()
            o.raw = area.raw
            o.name = area.name
            o.rid = area.rid
            return o

        area = LCArea()
        area.raw = random_str()
        area.name = random_str()
        area.rid = random_str()
        (ret, inserted) = self.lc.try_insert(area, 'rid', save, LCArea)
        self.assertEquals(ret, ExecState.CREATE)
        self.assertTrue(inserted.is_existed())
        delete(inserted)

    def test_try_insert_update(self):
        """insert objects but exists, update it."""
        def save(o):
            o.raw = arean.raw
            o.name = arean.name
            o.rid = arean.rid
            return o

        area = LCArea()
        area.raw = random_str()
        area.name = random_str()
        area.rid = random_str()
        area.save()
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
        area = LCArea()
        area.raw = random_str()
        area.name = random_str()
        area.rid = random_str()
        (ret, _) = self.lc.add_area(area, 'id')
        self.assertEquals(ret, ExecState.CREATE)
        delete(area)

    def test_add_area_id_exist(self):
        """add_area compared by id and exist so update it."""
        area = LCArea()
        area.raw = random_str()
        area.name = random_str()
        area.rid = random_str()
        area.save()
        id = area.id  # get new id
        area = LCArea.create_without_data(id)
        area.raw = random_str()
        area.name = random_str()
        area.rid = random_str()
        (ret, updated) = self.lc.add_area(area, 'id')
        self.assertEquals(ret, ExecState.UPDATE)
        self.assertEquals(updated.name, area.name)
        delete(area)

    def test_add_area_rid_unexist(self):
        """add_area compared by rid and unexist so create it."""
        area = LCArea()  # has been deleted
        area.raw = random_str()
        area.name = random_str()
        area.rid = random_str()
        (ret, inserted) = self.lc.add_area(area, 'rid')
        self.assertEquals(ret, ExecState.CREATE)
        self.assertEquals(inserted.rid, area.rid)
        delete(area)

    def test_add_area_rid_exist(self):
        """add_area compared by rid and unexist so update it."""
        area = LCArea()
        area.raw = random_str()
        area.name = random_str()
        area.rid = random_str()
        area.save()
        arean = LCArea()
        arean.raw = random_str()
        arean.name = random_str()
        arean.rid = area.rid
        (ret, updated) = self.lc.add_area(arean, 'rid')
        self.assertEquals(ret, ExecState.UPDATE)
        self.assertEquals(updated.name, arean.name)
        delete(updated)
