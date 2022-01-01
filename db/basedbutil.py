from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List, Optional

from crawler.model.location import AreaInfo, PortInfo
from crawler.model.tide import Tide, TideDay, TideLimit

from db.common import ExecState


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
    def add_area(self, area: AreaInfo) -> ExecState:
        """Add an area info or update it if exists"""
        pass

    @abstractmethod
    def add_port(self, port: PortInfo) -> ExecState:
        """Add a port info or update it if exists"""
        pass

    @abstractmethod
    def add_tide(self, day: TideDay, limit: TideLimit, port_id: str,  zone: str = "+8:00", datum: float = 0.0, date: date = datetime.now().date()) -> ExecState:
        """Add a tide record"""
        pass

    @abstractmethod
    def get_area(self, area_id: str) -> Optional[AreaInfo]:
        """
        Get :class:`AreaInfo` by :param:`area_id`

        :param area_id: Id of :class:`AreaInfo`
        :return: :class:`AreaInfo` or :class:`None` if not found
        """
        pass

    @abstractmethod
    def get_port(self, port_id: str = None) -> Optional[PortInfo]:
        """
        Get :class:`PortInfo` by :param:`port_id`

        :param port_id: Id of :class:`PortInfo`
        :return: :class:`PortInfo` or :class:`None` if not found
        """
        pass

    @abstractmethod
    def get_tide(self, port_id: str, date: date) -> Optional[Tide]:
        """
        Get :class:`Tide` of specified date and port

        :param port_id: Id of :class:`PortInfo`
        :param date: Specified date
        :return: :class:`Tide` or :class:`None` if not found
        """
        pass

    @abstractmethod
    def get_all_areas(self) -> List[AreaInfo]:
        """Get all :class:`AreaInfo`s"""
        pass

    @abstractmethod
    def get_all_ports(self) -> List[PortInfo]:
        """Get all :class:`PortInfo`s"""
        pass
