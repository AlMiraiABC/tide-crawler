import json
from datetime import date
from typing import Tuple, List

import requests

from config import HEADERS
from util.time import Timestamp


class TideLimit:
    """潮汐极值（最高点、最低点）"""

    def __init__(self, timestamp: float, high: float):
        """
        :param timestamp: 时间戳
        :param high: 潮高
        """
        self.timestamp = timestamp
        self.high = high

    def __str__(self):
        return json.dumps(self.__dict__)


class TideData(TideLimit):
    """潮汐24h数据"""


class TideInfo:
    """潮汐其他信息（时区、基准点）"""

    def __init__(self, zone: str, datum: float):
        """
        :param zone: 时区
        :param datum: 基准点
        """
        self.zone = zone
        self.datum = datum

    def __str__(self):
        return json.dumps(self.__dict__)


class GetTide:

    @staticmethod
    def data(port_id: int, query_date: date) -> Tuple[List[TideLimit], List[TideData], TideInfo]:
        """
        查询某天24h的潮高、极值、其他信息

        :param port_id: 港口id
        :param query_date: 日期
        """

        def timestamp(t: str) -> float:
            return Timestamp.comb_date_time_to_timestamp(str(query_date), t)

        # "https://www.cnss.com.cn/u/cms/www/tideJson/1_2020-04-12.json?v=1586699341746"
        base_url = f"https://www.cnss.com.cn/u/cms/www/tideJson/{port_id}_{str(query_date)}.json?"
        print(base_url)
        params = {
            'v': Timestamp.timestamp_to_spec()
        }
        response = requests.get(url=base_url, headers=HEADERS, params=params)
        contents = response.json()[0]

        # 确定timeAndLevel
        time_levels_content: List[dict] = contents['timeAndLevel']
        tide_limits = []
        for time_level in time_levels_content:
            tide_limits.append(TideLimit(timestamp(time_level.get('time')), float(time_level.get('tide_level'))))
        # 确定data
        datas_content: List[list] = contents['data']
        tide_datas = []
        for data in datas_content:
            tide_datas.append(TideData(Timestamp.spec_to_timestamp(float(data[0])), float(data[1])))
        # 确定port
        ports_content = contents['port']
        tide_info = TideInfo(ports_content['timeZone'], float(ports_content['tideDatum']))
        return tide_limits, tide_datas, tide_info
