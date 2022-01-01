import json
from datetime import date, datetime
from typing import List

"""Models for tide"""


class TideBase:
    """Base model for tide datas"""

    def __str__(self):
        return json.dumps(self.__dict__)


class TideData(TideBase):
    """潮汐数据"""

    def __init__(self, time: datetime.time, height: float):
        """
        :param time: 时间
        :param height: 潮高
        """
        self.time = time
        self.height = height


class TideDay(List[TideData], TideBase):
    """潮汐24h数据"""
    pass


class TideLimit(List[TideData], TideBase):
    """潮汐极值"""
    pass


class Tide(TideBase):

    def __init__(self, day: TideDay, limit: TideLimit, zone: str, datum: float, port_id: str, date: date = datetime.now().date()) -> None:
        """
        :param zone: 时区
        :param datum: 基准点
        :param port_id: 港口ID
        :param date: 日期
        """
        self.day = day
        self.limit = limit
        self.zone = zone
        self.datum = datum
        self.port_id = port_id
        self.date = date
