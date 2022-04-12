import re
from datetime import date, datetime, time
from typing import Any, Dict, List, Optional, Tuple, Union

import aiohttp
from config import Headers
# from db.basedbutil import IDT
# from db.dbutil import DbUtil
from storages.model import Area, Port, Province, Tide, TideItem
from utils.logger import Logger

from crawlers.c_model import CArea, CPort, CProvince, CTide
from utils.validate import Value


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

    async def __err_msg(self, method: str, url: str, response: aiohttp.ClientResponse) -> str:
        return f"{method} {url} <{response.status}><{await response.text()}>"

    async def __info_msg(self, method: str, url: str, response: aiohttp.ClientResponse) -> str:
        return f"{method} {url} <{await response.text()}>"

    async def get_tide(self, port_code: str, query_date: date = datetime.now().date()) -> Optional[Tide]:
        """
        Query tide infos of specified port and date.

        :param port_code: Port id or code.
        :param query_date: Queried date
        :return: Return None if failed.
        """
        if Value.is_any_none_or_empty(query_date) or Value.is_any_none_or_whitespace(port_code):
            raise ValueError(
                'port_code and query_date cannot be none or empty.')
        url = f'{Nmdis.__BASE_URL}/chaoxidata/list'
        reqbody = {
            'serchdate': query_date.strftime('%Y-%m-%d'),  # yyyy-MM-dd
            'sitecode': port_code
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, headers=Headers.NMDIS, json=reqbody) as response:
                if response.status != 200:
                    self.logger.error(await self.__err_msg('post', url, response))
                    return None
                self.logger.info(self.__info_msg('post', url, response))
                content: Dict[str, Any] = await response.json()
                datas = content.get('data')
                if not content.get('success') or not isinstance(datas, list) or len(datas) == 0:
                    self.logger.error(f'{content}')
                    return None
                data: Dict[str, Any] = datas[0]
                filedata: Dict[str, Union[int, str]] = data.get('filedata')
                day, limit = self.__get_tide_data(filedata)
                datum = self.__get_datum(data.get('benchmark'))
                # zone: str = data.get('timearea')
                tide = CTide()
                tide.date = datetime.fromisoformat(
                    data.get('serchdate'))  # YES, It's serchdate
                tide.day = day
                tide.limit = limit
                tide.datum = datum
                tide.port = CPort()
                tide.port.rid = port_code
                # tide.port = DbUtil().get_port(port_code, IDT.RID)
                tide.raw = await response.text()
                return tide

    async def get_provinces(self, area_code: str) -> Optional[List[Province]]:
        """
        Get all provinces belongs to area.

        :param area_code: Area id or code.
        :return: Return None if failed.
        """
        if Value.is_any_none_or_whitespace(area_code):
            raise ValueError(f'area_code cannot be none or empty.')
        url = f'{Nmdis.__BASE_URL}/area/list?parentId={area_code}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=Headers.NMDIS) as response:
                if response.status != 200:
                    self.logger.error(self.__err_msg('get', url, response))
                    return None
                self.logger.info(self.__info_msg('get', url, response))
                content = await response.json()
                if not content.get('success') or not isinstance(content.get('data'), list):
                    self.logger.error(f'{content}')
                    return None
                provinces: List[Province] = []
                data: List[Dict[str, Any]] = content.get('data')
                for item in data:
                    province = CProvince()
                    province.rid = item.get('id')
                    province.name = item.get('areaname')
                    province.raw = await response.text()
                    province.area = CArea()
                    province.area.rid = area_code
                    # province.area = DbUtil().get_area(area_code, IDT.RID)
                    provinces.append(province)
                return provinces

    async def get_areas(self) -> Optional[List[Area]]:
        """
        Get all areas.

        :return: Return None if failed.
        """
        url = f'{Nmdis.__BASE_URL}/area/list'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=Headers.NMDIS) as response:
                if response.status != 200:
                    self.logger.error(self.__err_msg('get', url, response))
                    return None
                self.logger.info(self.__info_msg('get', url, response))
                content = await response.json()
                if not content.get('success') or not isinstance(content.get('data'), list):
                    self.logger.error(f'{content}')
                    return None
                areas: List[Area] = []
                data: List[Dict[str, Any]] = content.get('data')
                for item in data:
                    area = CArea()
                    area.rid = item.get('id')
                    area.raw = await response.text()
                    area.name = item.get('areaname')
                    areas.append(area)
                return areas

    async def get_ports(self, province_code: str) -> Optional[List[Port]]:
        """
        Get all ports belongs to province.

        :param province_code: Province id or code.
        :return: Return None if failed.
        """
        if Value.is_any_none_or_whitespace(province_code):
            raise ValueError(f'province_code cannot be none or empty.')
        url = f'{Nmdis.__BASE_URL}/site/list?areaId={province_code}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=Headers.NMDIS) as response:
                if response.status != 200:
                    self.logger.error(self.__err_msg('get', url, response))
                    return None
                self.logger.info(self.__info_msg('get', url, response))
                content: dict = await response.json()
                if not content.get('success') or not isinstance(content.get('data'), list):
                    self.logger.error(f'{content}')
                    return None
                ports: List[Port] = []
                data: List[Dict[str, Any]] = content.get('data')
                for item in data:
                    port = CPort()
                    port.rid = item.get('code')
                    port.name = item.get('name')
                    port.raw = await response.text()
                    port.province = CProvince()
                    port.province.rid = province_code
                    port.geopoint = (item.get('coordx'), item.get('coordy'))
                    port.zone = ''  # TODO: get time zone from get_tide response.data.timearea
                    ports.append(port)
                return ports

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
