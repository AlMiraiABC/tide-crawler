from unittest import TestCase

import leancloud

from db.leancloud.lc_util import LCUtil


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
