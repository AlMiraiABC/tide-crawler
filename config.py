import logging
from enum import Enum, auto
from typing import Optional


class Storages(Enum):
    """Storage engines, where to save data"""
    LEAN_CLOUD = auto()  # leancloud storage https://www.leancloud.cn/storage/
    RDB = auto()  # Relational Database


class Crawlers(Enum):
    """Crawler engines, where data come from"""
    CXB = auto()  # https://www.chaoxibiao.net/
    CNSS = auto()  # https://www.cnss.com.cn/tide/
    NMDIS = auto()  # http://mds.nmdis.org.cn/pages/tidalCurrent.html


STORAGE: Storages = Storages.LEAN_CLOUD

CRAWLER: Crawlers = Crawlers.NMDIS


class LCSetting:
    """
    settings to connect [LeanCloud Data Storage](https://console.leancloud.cn/apps/{AppId}/storage/data)
    """
    APP_ID: str = "Gu2SvkoBC8noi8OKlSLCvuRt-gzGzoHsz"
    # `APP_KEY` and `MASTER_KEY` cannot be empty or none at the same time
    APP_KEY: Optional[str] = "8lo2qnnkjVku2rq1g00Qh38F"
    # `APP_KEY` and `MASTER_KEY` cannot be empty or none at the same time
    MASTER_KEY: Optional[str] = None
    # username of spider in class _User
    USERNAME = 'spider'
    # password of spider in class _User
    PASSWORD = 'TideSpider'
    # logging level, will print log to console window
    # please close this when in prod env.
    DEBUG_LEVEL = logging.DEBUG


class RDBSetting:
    """
    settings to connect relational database

    See also
    ------
    * https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls
    * https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Engine
    """
    DIALECT: str = 'mysql'
    DRIVER: Optional[str] = 'pymysql'
    HOST: str = 'db.nmtsoft.net'
    PORT: Optional[int] = 3306
    USERNAME: str = 'tide_root'
    PASSWORD: str = 'os)3zaaK4Z_rq?}_'
    DATABASE: str = 'tide'
    KWARGS = {}  # https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Engine


class Headers:
    """
    headers for crawler
    """
    # get data from [海事服务网](https://www.cnss.com.cn/tide/)
    CNSS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/80.0.3987.163 Safari/537.36 ',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.cnss.com.cn/tide/',
        'Accept': 'application/json, text/javascript, */*; q=0.01'
    }
    # get data from [大鱼潮汐表](https://www.chaoxibiao.net/)
    CXB = {

    }


class LoggerSetting:
    """settings for log"""
    LOGGING_FILE = 'logging.yaml'
