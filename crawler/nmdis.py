import re
from datetime import date, time
from typing import Any, Dict, Tuple, Union

import requests
from config import Headers
from util.logger import Logger

from crawler.model.tide import Tide, TideData, TideDay, TideLimit


class Nmdis:
    """国家海洋科学数据中心"""

    __BASE_URL: str = 'http://mds.nmdis.org.cn/'

    def __init__(self) -> None:
        self.logger = Logger(self.__class__.__name__).logger

    def get_tide(self, port_code: str, query_date: date) -> Tide:
        """
        查询某天24h的潮高、极值、其他信息

        :param port_code: 港口编号
        :param query_date: 日期
        :return: [TideLimit, TideDay, TideInfo]
        """
        url = f'{Nmdis.__BASE_URL}/service/rdata/front/knowledge/chaoxidata/list'
        print(url)
        reqbody = {
            'serchdate': query_date.strftime('%Y-%m-%d'),  # yyyy-MM-dd
            'sitecode': port_code
        }
        response = requests.post(url=url, headers=Headers, json=reqbody)
        # region verify
        if response.status_code != 200:
            self.logger.error(f"{response.status_code}<{response.text}>")
            return
        content: Dict[str, Any] = response.json()
        if not content.get('success'):
            self.logger.error(f'{content}')
        # endregion
        data: Dict[str, Any] = content.get('data')[0]
        filedata: Dict[str, Union[int, str]] = data.get('filedata')
        day, limit = self.__get_tide_data(filedata)
        # region get tide infos
        datum = self.__get_datum(data.get('benchmark'))
        zone: str = data.get('timearea')
        return Tide(day, limit, zone, datum, port_code, query_date)
        # endregion
        return limit, day, info

        # endregion

    def __get_datum(self, text: str) -> float:
        """
        Get datum from string benchmark

        :param text: Benchmark string
        :return: Datum, or `0.0` if not match pattern
        """
        pattern = '[上,下](\d+)'
        regex = re.search(pattern, text)
        if not regex:
            return 0.0
        h = float(regex.group(2))
        return h if regex.group(1) == '上' else -h

    def __get_tide_data(self, data: Dict[str, Union[int, str]]) -> Tuple[TideDay, TideLimit]:
        day = [TideData(time(re.search('\d+', k).group()), v)
               for k, v in data.items() if re.match('a\d+', k)]
        limit = [TideData(time.fromisoformat(data.get('cs'+re.search("\\d+", k).group())), v)
                 for k, v in data.items() if re.match('cg\d+', k)]
        return day, limit
