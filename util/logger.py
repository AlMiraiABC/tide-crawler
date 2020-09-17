import logging
import os
import sys
import time
from logging.handlers import TimedRotatingFileHandler

from config import LoggerSetting


def _package_name(path: str) -> str:
    """
    获得包名和文件名

    :param path: 一个含项目名到指定文件名的路径。

        可通过``sys._getframe(1).f_code.co_filename获取当前文件的路径``
    :return: 包名及文件名(不含扩展名)

    example:
        >>> _package_name('D:\\TideCrawler\\log\\backend\\dao.py')
        'log/backend/dao'
    """
    path = path.replace('\\', '/')
    path = path[:path.rfind('.')]
    p = path.split('/')
    return '/'.join(p[p.index('TideCrawler') + 1:])


class Logger:
    """
    自定义Logger

    将信息和错误信息输出至控制台和对应日志文件
    """

    def __init__(self, class_name: str, log_formatter: logging.Formatter = None):
        """
        :param class_name 类名, 用于日志的归类文件夹
        :param log_formatter: 格式化参数，为空时，使用默认参数 LoggerSetting.Formatter
        """
        # 调用该Logger的文件路径
        log_path: str = _package_name(sys._getframe(1).f_code.co_filename)
        # 将``包名.文件名.class_name``作为Logger名
        self.logger = logging.getLogger(log_path.replace('/', '.') + '.' + class_name)
        if not self.logger.handlers:
            # set handler
            # 控制台输出
            self.logger.setLevel(LoggerSetting.LEVEL)
            self.log_console = logging.StreamHandler()
            self.when = LoggerSetting.WHEN
            self.backup_count = LoggerSetting.BACKUP_COUNT
            self.encoding = LoggerSetting.ENCODING
            if log_formatter is None:
                log_formatter = logging.Formatter(fmt=LoggerSetting.FORMATTER, datefmt=LoggerSetting.DATEFMT)
            self.log_console.setFormatter(log_formatter)
            # add handler
            # 保存为日志文件，路径为log/包名/类名/yyyy-mm-dd.log
            self.path: str = f'log/{log_path}/{class_name}/'
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            filename: str = self.path + time.strftime('%F') + '.log'
            log_file = TimedRotatingFileHandler(filename, when=self.when, backupCount=self.backup_count,
                                                encoding=self.encoding)
            log_file.setFormatter(log_formatter)
            self.logger.addHandler(self.log_console)
            self.logger.addHandler(log_file)
