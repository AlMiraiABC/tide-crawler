from datetime import date, datetime
from typing import List, Optional, Tuple

from leancloud.object_ import Object

from config import STORAGE, Storages
from util.singleton import Singleton

from db.basedbutil import BaseDbUtil
from db.common import ExecState
from db.leancloud.lc_util import LCUtil
from db.model import Area, Port, Tide, TideItem
from db.rdb.rdb_util import RDBUtil
from util.validate import Value


class DbUtil(BaseDbUtil):
    """Wrapper for all DAOs"""

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

    def add_port(self, port: Port) -> Tuple[ExecState, Port]:
        self.__valid_none(port, 'port')
        if Value.is_null_or_whitespace(port.rid, port.name, port.area, port.area.rid):
            raise AttributeError(
                "port rid, name, area and area.rid cannot be null or empty")
        return self.db_util.add_port(port)

    def add_area(self, area: Area) -> Tuple[ExecState, Area]:
        self.__valid_none(area, 'area')
        if Value.is_null_or_whitespace(area.rid, area.name):
            raise AttributeError("area rid and name cannot be null or empty")
        return self.db_util.add_area(area)

    def add_tide(self, tide: Tide) -> Tuple[ExecState, Tide]:
        self.__valid_none(tide, 'tide')
        if Value.is_null_or_whitespace(tide.port, tide.port.rid):
            raise AttributeError("tide port and port.rid cannot be null or empty")
        return self.db_util.add_tide(tide)

    def get_area(self, area_id: str) -> Optional[Area]:
        return self.db_util.get_area(area_id)

    def get_port(self, port_id: str = None) -> Optional[Area]:
        return self.db_util.get_port(port_id=port_id)

    def get_tide(self, port_id: str, date: date) -> Optional[Tide]:
        return self.db_util.get_tide(port_id, date)

    def get_all_areas(self) -> List[Area]:
        return self.db_util.get_all_areas()

    def get_all_ports(self) -> List[Port]:
        return self.db_util.get_all_ports()


db_util: DbUtil = Singleton(DbUtil)
