import json
from datetime import time
from typing import List

"""Models for tide"""

class TideBase:
    """Base model for tide datas"""
    def __str__(self):
        return json.dumps(self.__dict__)


class TideData(TideBase):
    """潮汐数据"""

    def __init__(self, time: time, height: float):
        """
        :param time: 时间
        :param height: 潮高
        """
        self.time = time
        self.height = height


class TideDay(List[TideData], TideBase):
    """潮汐24h数据"""


class TideLimit(List[TideData], TideBase):
    """潮汐极值"""


class TideInfo(TideBase):
    """潮汐其他信息"""

    def __init__(self, zone: str, datum: float):
        """
        :param zone: 时区
        :param datum: 基准点
        """
        self.zone = zone
        self.datum = datum
