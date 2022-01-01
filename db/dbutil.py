from datetime import date, datetime
from typing import List, Optional

from config import STORAGE, Storages
from crawler.model.location import AreaInfo, PortInfo
from crawler.model.tide import Tide, TideDay, TideLimit
from util.singleton import Singleton

from db.basedbutil import BaseDbUtil
from db.common import ExecState
from db.leancloud.lc_util import LCUtil
from db.rdb.rdb_util import RDBUtil


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

    def add_port(self, port: PortInfo) -> ExecState:
        return self.add_port(port)

    def add_area(self, area: AreaInfo) -> ExecState:
        return self.db_util.add_area(area)

    def add_tide(self, day: TideDay, limit: TideLimit, port_id: str, zone: str = "+8:00", datum: float = 0, date: date = datetime.now().date()) -> ExecState:
        return self.add_tide(day, limit, port_id, zone=zone, datum=datum, date=date)

    def get_area(self, area_id: str) -> Optional[AreaInfo]:
        return self.get_area(area_id)

    def get_port(self, port_id: str = None) -> Optional[PortInfo]:
        return self.get_port(port_id=port_id)

    def get_tide(self, port_id: str, date: date) -> Optional[Tide]:
        return self.get_tide(port_id, date)

    def get_all_areas(self) -> List[AreaInfo]:
        return self.get_all_areas()

    def get_all_ports(self) -> List[PortInfo]:
        return self.get_all_ports()


db_util: DbUtil = Singleton(DbUtil)
