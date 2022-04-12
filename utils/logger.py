import logging
import logging.config
import sys

import yaml
from config import LoggerSetting


def _package_name(path: str, project_name: str = 'TideCrawler') -> str:
    """
    get package name

    :param path: path from :param:``project_name`` to file, must incude :param:``project_name``. such as: ``TideCrawler/a/b/c.py``. get file path from ``sys._getframe(1).f_code.co_filename``
    :param project_name: project_name.
    :return: package_name.file_name_without_ext

    example
    ------
    >>> _package_name('TideCrawler/a/b/c.py')
    'a.b.c'
    """
    path = path.replace('\\', '/')
    path = path[:path.rfind('.')]
    p = path.split('/')
    return '.'.join(p[p.index(project_name) + 1:])


class Logger:
    """
    自定义Logger

    将信息和错误信息输出至控制台和对应日志文件
    """

    def __init__(self, class_name: str, logging_config: str = LoggerSetting.LOGGING_FILE):
        """
        :param class_name: 类名
        """
        # get caller's path
        log_path: str = _package_name(sys._getframe(1).f_code.co_filename)
        with open(logging_config, "r") as f:
            config = yaml.load(f,yaml.Loader)
            logging.config.dictConfig(config)
        # 将``包名.文件名.class_name``作为Logger名
        self.logger = logging.getLogger(f'{log_path}.{class_name}')
