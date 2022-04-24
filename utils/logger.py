import logging
import logging.config
import os
import sys

import yaml
from config import LoggerSetting


def _package_name(path: str, project_name: str = None) -> str:
    """
    get package name

    :param path:
        Path from :param:``project_name`` to file.
        Should contain :param:``project_name`` at first, such as: ``<project_name>/a/b/c.py``.
        Get file path from ``sys._getframe(1).f_code.co_filename``
    :param project_name: project_name. Current project folder name by default.
    :return: package_name.file_name_without_ext. If :param:`path` not contain :param:`project_name`, it return `<project_name>.default`

    example
    ------
    >>> _package_name('<peoject_name>/a/b/c.py')
    'a.b.c'
    """
    project_name = project_name if project_name else os.path.basename(
        os.getcwd())
    path = path.replace('\\', '/')
    path = path[:path.rfind('.')]
    p = path.split('/')
    if project_name in p:
        return '.'.join(p[p.index(project_name) + 1:])
    return f'{project_name}.default'


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
            config = yaml.load(f, yaml.Loader)
            logging.config.dictConfig(config)
        # 将``包名.文件名.class_name``作为Logger名
        self.logger = logging.getLogger(f'{log_path}.{class_name}')
