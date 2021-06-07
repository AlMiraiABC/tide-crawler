from unittest import TestCase

from util.logger import Logger


class TestLogger(TestCase):
    def test_log(self):
        log = Logger(self.__class__.__name__).logger
        log.info("TestInfo")
        log.error("TestError")
        log.warning("TestWarn")
