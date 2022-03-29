from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional


from db.common import ExecState
from db.model import Area, Port, Tide


class BaseDbUtil(ABC):
    """DAO base class"""

    @abstractmethod
    def open(self):
        """Open a connection or reopen a new connection if it closed."""
        pass

    @abstractmethod
    def close(self):
        """Close current connection"""
        pass

    @abstractmethod
    def add_area(self, area: Area) -> ExecState:
        """Add an area or update it if exists"""
        pass

    @abstractmethod
    def add_port(self, port: Port) -> ExecState:
        """Add a port or update it if exists"""
        pass

    @abstractmethod
    def add_tide(self, Tide) -> ExecState:
        """Add a tide record"""
        pass

    @abstractmethod
    def get_area(self, area_id: str) -> Optional[Area]:
        """
        Get :class:`CArea` by :param:`area_id`

        :param area_id: Id of :class:`Area`
        :return: :class:`Area` or :class:`None` if not found
        """
        pass

    @abstractmethod
    def get_port(self, port_id: str = None) -> Optional[Port]:
        """
        Get :class:`Port` by :param:`port_id`

        :param port_id: Id of :class:`Port`
        :return: :class:`Port` or :class:`None` if not found
        """
        pass

    @abstractmethod
    def get_tide(self, port_id: str, date: date) -> Optional[Tide]:
        """
        Get :class:`Tide` of specified date and port

        :param port_id: Id of :class:`Port`
        :param date: Specified date
        :return: :class:`Tide` or :class:`None` if not found
        """
        pass

    @abstractmethod
    def get_all_areas(self) -> List[Area]:
        """Get all :class:`Area`s"""
        pass

    @abstractmethod
    def get_all_ports(self) -> List[Port]:
        """Get all :class:`Port`s"""
        pass
