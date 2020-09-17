import logging


class DatabaseSetting:
    HOST: str = '182.92.206.138'
    PORT: int = 3306
    USERNAME: str = 'tide'
    PASSWORD: str = 'tide'
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
    """日志"""
    FORMATTER = '%(asctime)s:%(levelname)s:' \
                '%(pathname)s:%(funcName)s:%(message)s'  # 日志格式
    DATEFMT = '%Y/%m/%d %H:%M:%S'  # asctime格式
    LEVEL = logging.INFO  # 日志输出等级
    WHEN = 'W0'  # 周一
    BACKUP_COUNT = 14  # 保存天数
    ENCODING = 'utf-8'  # 日志文件字符集
