from abc import ABC, abstractmethod

from config import STORAGE, Storages
from util.singleton import Singleton

from db.common import ExecState
from db.leancloud.lc_util import LCUtil
from db.port import AreaInfo, PortInfo
from db.rdb.rdb_util import RDBUtil
from db.tide import TideDay, TideInfo, TideLimit


class BaseDbUtil(ABC):
    @abstractmethod
    def open(self):
        """Open a connection or reopen a new connection if it closed."""
        pass

    @abstractmethod
    def close(self):
        """Close current connection"""
        pass

    @abstractmethod
    def add_port(self, port: PortInfo) -> ExecState:
        """Add a port info or update it if exists"""
        pass

    @abstractmethod
    def add_tide(self, info: TideInfo, day: TideDay, limit: TideLimit) -> ExecState:
        """Add a tide record"""
        pass

    @abstractmethod
    def add_area(self, area: AreaInfo) -> ExecState:
        """Add an area info or update it if exists"""
        pass


class __DbUtil(BaseDbUtil):
    def __init__(self) -> None:
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

    def add_tide(self, info: TideInfo, day: TideDay, limit: TideLimit) -> ExecState:
        return self.db_util.add_tide(info, day, limit)


db_util: __DbUtil = Singleton(__DbUtil)
