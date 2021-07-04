import logging


class DatabaseSetting:
    HOST: str = 'db.nmtsoft.net'
    PORT: int = 3306
    USERNAME: str = 'tide_root'
    PASSWORD: str = 'os)3zaaK4Z_rq?}_'
    DATABASE: str = 'tide'
    CHARSET: str = 'utf8'


# 爬虫的HEADER
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.163 Safari/537.36 ',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://www.cnss.com.cn/tide/',
    'Accept': 'application/json, text/javascript, */*; q=0.01'
}


class LoggerSetting:
    """settings for log"""
    LOGGING_FILE = 'logging.yaml'
