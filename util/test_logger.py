import os
from unittest import TestCase
from util.logger import Logger, _package_name
import re


def verify_log(level: str, message: str, log: str, fun: str, type: str = 'info') -> bool:
    extra = r'' if type is None or type.lower(
    ) == 'info' else r'\d{2}:\d*-\d*:'
    pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+\[' + \
        level + r'\].*?\\util\\test_logger.py:'+fun+':'+extra+message
    return re.match(pattern, log) is not None


def clear_logs():
    """remove all log files"""
    ep = 'log/error'
    ip = 'log/info'
    efs = os.listdir(ep)
    for e in efs:
        os.remove(os.path.join(ep, e))
    ifs = os.listdir(ip)
    for i in ifs:
        os.remove(os.path.join(ip, i))


class TestLogger(TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        self.logger = Logger(self.__class__.__name__).logger

    @classmethod
    def setUpClass(cls) -> None:
        """
        permission error when remove log files by code
        please remove these manually.
        """
        # clear_logs()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        # clear_logs()
        super().tearDownClass()

    def test_logfile_info(self):
        message = 'test log info'
        self.logger.info(message)
        with open('log/info/info.log') as f:
            log = f.readline()
            self.assertTrue(verify_log(
                'INFO', message, log, 'test_logfile_info'))

    def test_logfile_1_warning(self):
        message = 'test log warning'
        self.logger.warning(message)
        with open('log/error/error.log') as f:
            log = f.readlines()
            self.assertTrue(verify_log('WARNING', message,
                            log[0], 'test_logfile_1_warning', type='error'))

    def test_logfile_2_error(self):
        message = 'test log error'
        self.logger.error(message)
        with open('log/error/error.log') as f:
            log = f.readlines()
            self.assertTrue(verify_log('ERROR', message,
                            log[1], 'test_logfile_2_error', type='error'))

    def test__package_name_linux(self):
        p = _package_name('/TideCrawler/a/b/c.py')
        self.assertEquals(p, 'a.b.c')

    def test__package_name_win(self):
        p = _package_name('\\TideCrawler\\a\\b\\c.py')
        self.assertEquals(p, 'a.b.c')
