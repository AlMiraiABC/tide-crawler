from datetime import date
from typing import Any, List, Optional, Tuple, Type, TypeVar, Union

from services.crawler_service import CrawlerService
from storages.basedbutil import IDT, BaseDbUtil, switch_idt
from storages.common import ExecState
from storages.dbutil import DbUtil
from storages.model import Area, Port, Province, Tide, WithInfo
from utils.meta import merge_meta
from utils.singleton import Singleton
from utils.validate import Value
from config import CACHE, Caches

from utils.alru import alru_cache
from cache.dict_db import DictDb

_ClazzWithInfo = TypeVar('_ClazzWithInfo', bound=WithInfo)


EXECSTATE_SUCCESS = [ExecState.CREATE, ExecState.SUCCESS, ExecState.UPDATE]


class CacheUtil(merge_meta(BaseDbUtil, Singleton)):

    def __new__(cls: Type[DbUtil]) -> DbUtil:
        if CACHE == Caches.STORAGE:
            return DbUtil()
        return super().__new__(cls)

    def __init__(self) -> None:
        super().__init__()
        if CACHE == Caches.NMDIS:
            self.cache = DictDb()

    async def open(self):
        await super().open()

    async def close(self):
        await super().close()

    def cmp_area(self, c1: Area, c2: Area) -> bool:
        return self.__cmp_withinfo(c1, c2)

    def cmp_province(self, c1: Province, c2: Province) -> bool:
        return self.__cmp_withinfo(c1, c2)

    def cmp_port(self, c1: Port, c2: Port) -> bool:
        if not self.__cmp_withinfo(c1, c2):
            return False
        if c1.geopoint != c2.geopoint:
            return False
        if c1.zone != c2.zone:
            return False
        return True

    def __cmp_withinfo(self, c1: _ClazzWithInfo, c2: _ClazzWithInfo) -> bool:
        """
        Compare two area instance.

        :return: Different attributes.
        """
        cmpn = self.__cmp_base(c1, c2)
        if cmpn:
            return cmpn
        # optional objectId
        if not Value.is_any_none_or_whitespace(c1.objectId, c2.objectId):
            if c1.objectId != c2.objectId:
                return False
        else:
            if c1.rid != c2.rid:
                return False
            if c1.name != c2.name:
                return False
        return True

    def __cmp_base(self, o1, o2) -> Optional[bool]:
        """
        Base comparison for None, type and id.

        :return:
            True if both are None or has equals id.
            False if one of None or difference type.
            None for other situations and continue to compare.
        """
        if o1 is None and o2 is None:
            return True
        if o1 is None or o2 is None:
            return False
        if type(o1) != type(o2):
            return False
        if id(o1) == id(o2):
            return True
        return None

    def __valid_none(self, o: Any, name: str):
        if o is None:
            raise ValueError(f"{name} cannot be null")

    async def add_area(self, area: Area, col: IDT) -> Tuple[ExecState, Union[Optional[Area], Exception]]:
        self.__valid_none(area, 'area')
        if Value.is_any_none_or_whitespace(area.rid, area.name):
            raise ValueError("area rid and name cannot be null or empty")
        ca = self.cache.get_area(switch_idt(
            col, lambda: area.objectId, lambda: area.rid))
        if not self.__cmp_withinfo(ca, area):
            (ret, inserted) = await DbUtil().add_area(area, col)
            if ret in EXECSTATE_SUCCESS:
                self.cache._add_area(inserted)

    async def add_province(self, province: Province, col: IDT) -> Tuple[ExecState, Union[Optional[Province], Exception]]:
        self.__valid_none(province, 'port')
        if Value.is_any_none_or_whitespace(province.rid, province.name, province.area, province.area.rid):
            raise ValueError(
                "province rid, name, area and area.rid cannot be null or empty")
        pa = self.cache.get_province(switch_idt(
            col, lambda: province.objectId, lambda: province.rid))
        if not self.cmp_province(pa, province):
            (ret, inserted) = await DbUtil().add_province(province, col)
            if ret in EXECSTATE_SUCCESS:
                self.cache._add_province(inserted)

    async def add_port(self, port: Port, col: IDT) -> Tuple[ExecState, Union[Optional[Port], Exception]]:
        self.__valid_none(port, 'port')
        if Value.is_any_none_or_whitespace(port.rid, port.name, port.area, port.area.rid):
            raise ValueError(
                "port rid, name, area and area.rid cannot be null or empty")
        pa = self.cache.get_port(switch_idt(
            col, lambda: port.objectId, lambda: port.rid))
        if not self.cmp_port(pa, port):
            (ret, inserted) = await DbUtil().add_port(port, col)
            if ret in EXECSTATE_SUCCESS:
                self.cache._add_port(inserted)

    async def add_tide(self, tide: Tide, col: IDT) -> Tuple[ExecState, Union[Optional[Tide], Exception]]:
        self.__valid_none(tide, 'tide')
        if Value.is_any_none_or_whitespace(tide.port, tide.port.rid):
            raise ValueError(
                "tide port and port.rid cannot be null or empty")
        return await self.db_util.add_tide(tide, col)

    async def get_area(self, area_id: str, col: IDT) -> Optional[Area]:
        if Value.is_any_none_or_whitespace(area_id):
            raise ValueError("area_id cannot be null or empty.")
        return self.cache.get_area(area_id, col)

    async def get_province(self, province_id: str, col: IDT) -> Optional[Province]:
        if Value.is_any_none_or_whitespace(province_id):
            raise ValueError("province_id cannot be null or empty.")
        return self.cache.get_province(province_id, col)

    async def get_port(self, port_id: str, col: IDT) -> Optional[Port]:
        if Value.is_any_none_or_whitespace(port_id):
            raise ValueError("port_id cannot be null or empty.")
        return self.cache.get_port(port_id, col)

    @alru_cache(maxsize=1024, typed=True)
    async def get_tide(self, port_id: str, d: date) -> Optional[Tide]:
        if Value.is_any_none_or_whitespace(port_id):
            raise ValueError("port_id cannot be null or empty.")
        if d == None or d < date(2000, 0, 0):
            d = date.today()
        tide = await DbUtil().get_tide(port_id, d)
        if tide is not None:
            return tide
        port = await DbUtil().get_port(port_id, IDT.ID)
        return await CrawlerService().crawl_tide(d, port.rid)

    async def get_areas(self) -> List[Area]:
        return self.cache.get_areas()

    async def get_provinces(self, area_id: str, col: IDT = None) -> List[Province]:
        if Value.is_any_none_or_whitespace(area_id):
            raise ValueError("area_id cannot be null or empty")
        return self.cache.get_provinces(area_id, col)

    async def get_ports(self, province_id: str, col: IDT = None) -> List[Port]:
        if Value.is_any_none_or_whitespace(province_id):
            raise ValueError("province_id cannot be null or empty")
        return self.cache.get_ports(province_id, col)
