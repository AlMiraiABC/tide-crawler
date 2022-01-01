from unittest import TestCase

from db.leancloud.lc_util import LCUtil


class TestLCUtil(TestCase):
    def test_init(self):
        lc = LCUtil()
        print(lc)
        self.assertTrue(True)
