from abc import ABC, abstractmethod
from datetime import date
from enum import Enum, auto
from typing import Any, Callable, List, Optional, Tuple, Union

from storages.common import ExecState
from storages.model import Area, Port, Province, Tide


class IDT(Enum):
    """compared column"""
    ID = auto()
    RID = auto()


def switch_idt(idt: IDT, id_cb: Union[Callable[[], Any], Any] = lambda: None, rid_cb: Union[Callable[[], Any], Any] = lambda: None):
    """
    Switch for :class:`IDT`

    :param idt: Switched variable.
    :param id_cb: Call this when idt is 'ID' if it is callable. Or else return it directly.
    :param rid_cb: Call this when idt is 'RID' if it is callable. Or else return it directly.

    :throw ValueError: Cannot match :param:`idt`
    """
    if idt == IDT.ID:
        return id_cb() if callable(id_cb) else id_cb
    elif idt == IDT.RID:
        return rid_cb() if callable(id_cb) else rid_cb
    else:
        raise ValueError(f"idt must be 'id' or 'rid'")


class BaseDbUtil(ABC):
    """DAO base class"""

    @abstractmethod
    async def open(self):
        """Open a connection or reopen a new connection if it closed."""
        pass

    @abstractmethod
    async def close(self):
        """Close current connection"""
        pass

    @abstractmethod
    async def add_area(self, area: Area, col: IDT) -> Tuple[ExecState, Union[Area, Exception]]:
        """Add an area or update it if exists"""
        pass

    @abstractmethod
    async def add_province(self, province: Province, col: IDT) -> Tuple[ExecState, Optional[Province]]:
        """Add an province or update it if exists."""
        pass

    @abstractmethod
    async def add_port(self, port: Port, col: IDT) -> Tuple[ExecState, Optional[Port]]:
        """Add a port or update it if exists"""
        pass

    @abstractmethod
    async def add_tide(self, tide: Tide, col: IDT) -> Tuple[ExecState, Optional[Tide]]:
        """Add a tide record"""
        pass

    @abstractmethod
    async def get_area(self, area_id: str, col: IDT) -> Optional[Area]:
        """
        Get :class:`Area` by :param:`area_id`

        :param area_id: Id/objectId or rid of :class:`Area`
        :param col: Compared column.
        :return: :class:`Area` or :class:`None` if not found
        """
        pass

    @abstractmethod
    async def get_province(self, province_id: str, col: IDT) -> Optional[Province]:
        """
        Get :class:`Province` by :param:`province_id`

        :param province_id: Id/objectId or rid of :class:`Province`
        :param col: Compared column.
        :return: :class:`Province` or :class:`None` if not found
        """
        pass

    @abstractmethod
    async def get_port(self, port_id: str, col: IDT) -> Optional[Port]:
        """
        Get :class:`Port` by :param:`port_id`

        :param port_id: Id/objectId or rid of :class:`Port`
        :param col: Compared column.
        :return: :class:`Port` or :class:`None` if not found
        """
        pass

    @abstractmethod
    async def get_tide(self, port_id: str, d: date) -> Optional[Tide]:
        """
        Get :class:`Tide` of specified date and port

        :param port_id: Id/objectId or rid of :class:`Port`
        :param d: Specified date
        :param col: Compared column.
        :return: :class:`Tide` or :class:`None` if not found
        """
        pass

    @abstractmethod
    async def get_areas(self) -> List[Area]:
        """Get all :class:`Area`s"""
        pass

    @abstractmethod
    async def get_provinces(self, area: Union[Area, str], col: IDT = None) -> List[Province]:
        """
        Get all :class:`Province`s belongs to :param:`area`.

        :param area: :class:`Area` instance or :prop:`area.id`
        :param col: Compared column. It's required if type of :param:`area` is `str`
        """
        pass

    @abstractmethod
    async def get_ports(self, province: Union[Province, str], col: IDT = None) -> List[Port]:
        """
        Get all :class:`Port`s  belongs to:param:`province`.

        :param province: :class:`Province` instance or :prop:`province.id/objectId/rid`
        :param col: Compared column. It's required if type of :param:`province` is `str`
        """
        pass
