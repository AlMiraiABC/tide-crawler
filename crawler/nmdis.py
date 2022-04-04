import re
from datetime import date, datetime, time
from typing import Any, Dict, List, Tuple, Union

import aiohttp
import requests
from config import Headers
from db.basedbutil import IDT
from db.dbutil import DbUtil
from db.model import Area, Port, Province, Tide, TideItem, TideItemDict
from util.logger import Logger

from crawler.c_model import CArea, CPort, CProvince, CTide


class Nmdis:
    """
    国家海洋科学数据中心-潮汐潮流预报

    See More:
    -----------------
    http://mds.nmdis.org.cn/pages/tidalCurrent.html
    """

    __BASE_URL: str = 'http://mds.nmdis.org.cn/service/rdata/front/knowledge'

    def __init__(self) -> None:
        self.logger = Logger(self.__class__.__name__).logger

    async def get_tide(self, port_code: str, query_date: date = datetime.now().date()) -> Tide:
        """
        Query tide infos of specified port and date.

        :param port_code: port id or code.
        :param query_date: Queried date
        """
        url = f'{Nmdis.__BASE_URL}/chaoxidata/list'
        reqbody = {
            'serchdate': query_date.strftime('%Y-%m-%d'),  # yyyy-MM-dd
            'sitecode': port_code
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, headers=Headers.NMDIS, json=reqbody) as response:
                if response.status != 200:
                    self.logger.error(
                        f"post {url} <{response.status}><{await response.text()}>")
                    return
                self.logger.info(f"post {url} <{await response.text()}>")
                content: Dict[str, Any] = await response.json()
                if not content.get('success'):
                    self.logger.error(f'{content}')
                data: Dict[str, Any] = content.get('data')[0]
                filedata: Dict[str, Union[int, str]] = data.get('filedata')
                day, limit = self.__get_tide_data(filedata)
                datum = self.__get_datum(data.get('benchmark'))
                zone: str = data.get('timearea')
                tide = CTide()
                tide.day = day
                tide.limit = limit
                tide.zone = zone
                tide.datum = datum
                tide.port = DbUtil().get_port(port_code, IDT.RID)
                tide.raw = response.text
                return tide

    def get_provinces(self, area_code: str) -> List[Province]:
        """
        Get all provinces belongs to area.

        :param area_code: area id or code.
        """
        url = f'{Nmdis.__BASE_URL}/area/list?parentId={area_code}'
        resp = requests.get(url=url, headers=Headers)

    def __get_datum(self, text: str) -> float:
        """
        Get datum from string benchmark

        :param text: Benchmark string
        :return: Datum, or `0.0` if not match pattern
        """
        pattern = '([上,下])(\d+)'
        regex = re.search(pattern, text)
        if not regex or len(regex.regs) != 3:
            return 0.0
        h = float(regex.group(2))
        return h if regex.group(1) == '上' else -h

    def __get_tide_data(self, data: Dict[str, Union[int, str]]) -> Tuple[List[TideItem], List[TideItem]]:
        day = [TideItem(time(int(re.search('\d+', k).group())), v)
               for k, v in data.items() if re.match('a\d+', k)]
        limit = [TideItem(time.fromisoformat(data.get('cs'+re.search("\\d+", k).group())), v)
                 for k, v in data.items() if re.match('cg\d+', k)]
        return day, limit
