from db.db import lc_util
from unittest import TestCase
import leancloud


class TestLCUtil(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_1_init(self):
        """
        init and login successfully
        get current user
        """
        self.assertIsNotNone(leancloud.User.get_current())

    def test_2_logout(self):
        """
        logout successfully
        current user is none
        """
        lc_util.logout()
        self.assertIsNone(leancloud.User.get_current())

    def test_3_login(self):
        """
        login successfully when user is not login
        get current user
        """
        lc_util.login()
        self.assertIsNotNone(leancloud.User.get_current())

    def test_4_relogin(self):
        """
        do nothing when user has been logged in
        get current user
        """
        lc_util.login()
        self.assertIsNotNone(leancloud.User.get_current())
