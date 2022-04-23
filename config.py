import logging
import os
from typing import Optional


class LCSetting:
    """
    settings to connect [LeanCloud Data Storage](https://console.leancloud.cn/apps/{AppId}/storage/data)
    """
    APP_ID: str = os.environ.get('TC_LC_APP_ID')
    # `APP_KEY` and `MASTER_KEY` cannot be empty or none at the same time
    APP_KEY: Optional[str] = os.environ.get('TC_LC_APP_KEY')
    # `APP_KEY` and `MASTER_KEY` cannot be empty or none at the same time
    MASTER_KEY: Optional[str] = None
    # username of spider in class _User
    USERNAME = os.environ.get('TC_LC_UNAME')
    # password of spider in class _User
    PASSWORD = os.environ.get('TC_LC_UPW')
    # logging level, will print log to console window
    # please close this when in prod env.
    DEBUG_LEVEL = logging.DEBUG


class Headers:
    """
    headers for crawler
    """
    NMDIS = {

    }


class LoggerSetting:
    """settings for log"""
    LOGGING_FILE = 'logging.yaml'
