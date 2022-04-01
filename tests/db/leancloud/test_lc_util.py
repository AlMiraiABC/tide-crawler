from datetime import datetime
from os import remove
from unittest import TestCase

from db.common import ExecState
from db.leancloud.lc_model import LCArea
from db.leancloud.lc_util import LCUtil

import leancloud


def delete(*args):
    leancloud.Object.destroy_all(args)


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
        area.raw = 'abababab'
        area.name = 'test area'
        area.rid = '123'
        (ret, inserted) = self.lc.try_insert(area, 'rid', save, LCArea)
        self.assertEquals(ret, ExecState.CREATE)
        self.assertTrue(inserted.is_existed())
        delete(inserted)

    def test_try_insert_update(self):
        """insert objects but exists, update it."""
        def save(o):
            o = LCArea()
            o.raw = area.raw
            o.name = area.name
            o.rid = area.rid
            return o

        area = LCArea()
        area.raw = 'abababab'
        area.name = 'test area'
        area.rid = '123'
        area.save()
        NEW_NAME='test update area'
        area.name = NEW_NAME
        (ret, updated) = self.lc.try_insert(area, 'rid', save, LCArea)
        self.assertEquals(ret, ExecState.UPDATE)
        self.assertEquals(updated.name, NEW_NAME)
        delete(updated)
