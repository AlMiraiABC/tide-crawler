import time
from typing import Union
from datetime import date

"""
时间相关工具模块
"""


class Timestamp:
    """timestamp工具类"""

    @staticmethod
    def timestamp_to_spec(timestamp: float = time.time(), length: int = 13) -> float:
        """
        获得当前指定整数位的时间戳

        :param length 时间戳的长度
        :param timestamp 时间戳
        """
        current_time = round(timestamp * (10 ** (16 - length)))
        return current_time

    @staticmethod
    def spec_to_timestamp(timestamp: float = time.time(), length: int = 13) -> float:
        return timestamp / (10 ** (16 - length))

    @staticmethod
    def timestamp_to_datetime(timestamp: float, datetime_format='%Y-%m-%d %H:%M:%S', length: int = 13) -> str:
        """
        将时间戳转换为日期时间字符串

        :param length: 时间戳的长度
        :param datetime_format: 日期格式化
        :param timestamp: 时间戳
        :return: 日期时间字符串
        """
        return time.strftime(datetime_format, time.localtime(Timestamp.spec_to_timestamp(timestamp, length)))

    @staticmethod
    def comb_date_time_to_timestamp(str_date: Union[str, date],
                                    time_str: str,
                                    datetime_format='%Y-%m-%d %H:%M:%S') -> float:
        """
        合并日期字符串和时间字符串，并返回时间戳

        :param str_date: 日期字符串
        :param time_str: 时间字符串
        :param datetime_format: 合并的日期时间型字符串的格式
        :return: 时间戳
        """
        str_datetime: str = f'{str_date if type(str_date) == str else str(str_date)} {time_str}'
        return time.mktime(time.strptime(str_datetime, datetime_format))
