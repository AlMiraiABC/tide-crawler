from unittest import TestCase

from utils.logger import Logger, _package_name


class TestLogger(TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        self.logger = Logger(self.__class__.__name__).logger
        self.log_name = f'{__name__}.{self.__class__.__name__}'

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

    def __log_msg(self, level: str, message: str) -> str:
        return f'{level}:{self.log_name}:{message}'

    def test_logfile_info(self):
        message = 'test log info'
        with self.assertLogs(self.log_name) as logs:
            self.logger.info(message)
        self.assertEqual(logs.output, [self.__log_msg('INFO', message)])

    def test_logfile_warning(self):
        message = 'test log warning'
        with self.assertLogs(self.log_name) as logs:
            self.logger.warning(message)
        self.assertEqual(logs.output, [self.__log_msg('WARNING', message)])

    def test_logfile_error(self):
        message = 'test log error'
        with self.assertLogs(self.log_name) as logs:
            self.logger.error(message)
        self.assertEqual(logs.output, [self.__log_msg('ERROR', message)])

    def test__package_name_linux(self):
        p = _package_name('/TideCrawler/a/b/c.py')
        self.assertEqual(p, 'a.b.c')

    def test__package_name_win(self):
        p = _package_name('\\TideCrawler\\a\\b\\c.py')
        self.assertEqual(p, 'a.b.c')
