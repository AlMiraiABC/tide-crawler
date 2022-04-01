from datetime import date
from typing import List, Optional, Tuple, Union

from config import STORAGE, Storages
from util.singleton import Singleton
from util.validate import Value

from db.basedbutil import BaseDbUtil
from db.common import ExecState
from db.leancloud.lc_util import LCUtil
from db.model import Area, Port, Province, Tide
from db.rdb.rdb_util import RDBUtil
from leancloud.object_ import Object


class DbUtil(BaseDbUtil):
    """Wrapper for all storage operations."""

    def __init__(self) -> None:
        """Create a new dbutil instance. Please use `dbutil.db_util` as usual."""
        # TODO return db_util if has been created
        self.db_util: BaseDbUtil = None
        if STORAGE == Storages.LEAN_CLOUD:
            self.db_util = LCUtil()
        elif STORAGE == Storages.RDB:
            self.db_util = RDBUtil()
        else:
            raise ValueError(f"STORAGE {STORAGE} not support")

    def open(self):
        return self.db_util.open()

    def close(self):
        return self.db_util.close()

    def __valid_none(self, o: Object, name: str):
        if o is None:
            raise ValueError(f"{name} cannot be null")

    def add_area(self, area: Area) -> Tuple[ExecState, Area]:
        self.__valid_none(area, 'area')
        if Value.is_any_none_or_whitespace(area.rid, area.name):
            raise ValueError("area rid and name cannot be null or empty")
        return self.db_util.add_area(area)

    def add_province(self, province: Province) -> ExecState:
        self.__valid_none(province, 'port')
        if Value.is_any_none_or_whitespace(province.rid, province.name, province.area, province.area.rid):
            raise ValueError(
                "province rid, name, area and area.rid cannot be null or empty")
        return self.db_util.add_province(province)

    def add_port(self, port: Port) -> Tuple[ExecState, Port]:
        self.__valid_none(port, 'port')
        if Value.is_any_none_or_whitespace(port.rid, port.name, port.area, port.area.rid):
            raise ValueError(
                "port rid, name, area and area.rid cannot be null or empty")
        return self.db_util.add_port(port)

    def add_tide(self, tide: Tide) -> Tuple[ExecState, Tide]:
        self.__valid_none(tide, 'tide')
        if Value.is_any_none_or_whitespace(tide.port, tide.port.rid):
            raise ValueError(
                "tide port and port.rid cannot be null or empty")
        return self.db_util.add_tide(tide)

    def get_area(self, area_id: str) -> Optional[Area]:
        if Value.is_any_none_or_whitespace(area_id):
            raise ValueError("area_id cannot be null or empty.")
        return self.db_util.get_area(area_id)

    def get_province(self, province_id: str) -> Optional[Province]:
        if Value.is_any_none_or_whitespace(province_id):
            raise ValueError("province_id cannot be null or empty.")
        return self.db_util.get_province(province_id)

    def get_port(self, port_id: str) -> Optional[Area]:
        if Value.is_any_none_or_whitespace(port_id):
            raise ValueError("port_id cannot be null or empty.")
        return self.db_util.get_port(port_id)

    def get_tide(self, port_id: str, d: date) -> Optional[Tide]:
        if Value.is_any_none_or_whitespace(port_id):
            raise ValueError("port_id cannot be null or empty.")
        if d == None or d < date(2000, 0, 0):
            d = date.today()
        return self.db_util.get_tide(port_id, d)

    def get_areas(self) -> List[Area]:
        return self.db_util.get_all_areas()

    def get_provinces(self, area: Union[Area, str]) -> List[Province]:
        return self.db_util.get_provinces(area)

    def get_ports(self, province: Union[Province, str]) -> List[Port]:
        return self.db_util.get_ports(province)


db_util: DbUtil = Singleton(DbUtil)
