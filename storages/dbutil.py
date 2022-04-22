from datetime import date
from typing import Any, List, Optional, Tuple, Union

from config import STORAGE, Storages
from utils.meta import merge_meta
from utils.singleton import Singleton
from utils.validate import Value

from storages.basedbutil import IDT, BaseDbUtil
from storages.common import ExecState
from storages.leancloud.lc_util import LCUtil
from storages.model import Area, Port, Province, Tide
from storages.rdb.rdb_util import RDBUtil


class DbUtil(merge_meta(BaseDbUtil, Singleton)):
    """Wrapper for all storage operations."""

    def __init__(self, db_util: BaseDbUtil = None) -> None:
        """Create a new dbutil instance. Please use `dbutil.db_util` as usual."""
        self.db_util: BaseDbUtil = None
        if db_util:
            self.db_util = db_util
        else:
            if STORAGE == Storages.LEAN_CLOUD:
                self.db_util = LCUtil()
            elif STORAGE == Storages.RDB:
                self.db_util = RDBUtil()
            else:
                raise ValueError(f"STORAGE {STORAGE} not support")

    async def open(self):
        return await self.db_util.open()

    async def close(self):
        return await self.db_util.close()

    def __valid_none(self, o: Any, name: str):
        if o is None:
            raise ValueError(f"{name} cannot be null")

    async def add_area(self, area: Area, col: IDT) -> Tuple[ExecState, Union[Optional[Area], Exception]]:
        self.__valid_none(area, 'area')
        if Value.is_any_none_or_whitespace(area.rid, area.name):
            raise ValueError("area rid and name cannot be null or empty")
        return await self.db_util.add_area(area, col)

    async def add_province(self, province: Province, col: IDT) -> Tuple[ExecState, Union[Optional[Province], Exception]]:
        self.__valid_none(province, 'port')
        if Value.is_any_none_or_whitespace(province.rid, province.name, province.area, province.area.rid):
            raise ValueError(
                "province rid, name, area and area.rid cannot be null or empty")
        return await self.db_util.add_province(province, col)

    async def add_port(self, port: Port, col: IDT) -> Tuple[ExecState, Union[Optional[Port], Exception]]:
        self.__valid_none(port, 'port')
        if Value.is_any_none_or_whitespace(port.rid, port.name, port.province, port.province.rid):
            raise ValueError(
                "port rid, name, province and province.rid cannot be null or empty")
        return await self.db_util.add_port(port, col)

    async def add_tide(self, tide: Tide, col: IDT) -> Tuple[ExecState, Union[Optional[Tide], Exception]]:
        self.__valid_none(tide, 'tide')
        if Value.is_any_none_or_whitespace(tide.port, tide.port.rid):
            raise ValueError(
                "tide port and port.rid cannot be null or empty")
        return await self.db_util.add_tide(tide, col)

    async def get_area(self, area_id: str, col: IDT) -> Optional[Area]:
        if Value.is_any_none_or_whitespace(area_id):
            raise ValueError("area_id cannot be null or empty.")
        return await self.db_util.get_area(area_id, col)

    async def get_province(self, province_id: str, col: IDT) -> Optional[Province]:
        if Value.is_any_none_or_whitespace(province_id):
            raise ValueError("province_id cannot be null or empty.")
        return await self.db_util.get_province(province_id, col)

    async def get_port(self, port_id: str, col: IDT) -> Optional[Port]:
        if Value.is_any_none_or_whitespace(port_id):
            raise ValueError("port_id cannot be null or empty.")
        return await self.db_util.get_port(port_id, col)

    async def get_tide(self, port_id: str, d: date) -> Optional[Tide]:
        if Value.is_any_none_or_whitespace(port_id):
            raise ValueError("port_id cannot be null or empty.")
        if d == None or d < date(2000, 1, 1):
            d = date.today()
        return await self.db_util.get_tide(port_id, d)

    async def get_areas(self) -> List[Area]:
        return await self.db_util.get_areas()

    async def get_provinces(self, area: Union[Area, str], col: IDT = None) -> List[Province]:
        return await self.db_util.get_provinces(area, col)

    async def get_ports(self, province: Union[Province, str], col: IDT = None) -> List[Port]:
        return await self.db_util.get_ports(province, col)
