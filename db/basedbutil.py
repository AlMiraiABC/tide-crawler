from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Callable, List, Literal, Optional, Tuple, Union

from db.common import ExecState
from db.model import Area, BaseClazz, Port, Province, Tide

# compared column
IDT = Literal['rid', 'id']


def switch_idt(idt: IDT, id_cb: Union[Callable[[], Any], Any] = lambda: None, rid_cb: Union[Callable[[], Any], Any] = lambda: None):
    """
    Switch for :class:`IDT`

    :param idt: Switched variable.
    :param id_cb: Call this when idt is 'id' if it is callable. Or else return it directly.
    :param rid_cb: Call this when idt is 'rid' if it is callable. Or else return it directly.

    :throw ValueError: Cannot match :param:`idt`
    """
    if idt == 'id':
        return id_cb() if callable(id_cb) else id_cb
    elif idt == 'rid':
        return rid_cb() if callable(id_cb) else rid_cb
    else:
        raise ValueError(f"idt must be 'id' or 'rid'")


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
    def add_area(self, area: Area, col: IDT) -> Tuple[ExecState, Optional[Area]]:
        """Add an area or update it if exists"""
        pass

    @abstractmethod
    def add_province(self, province: Province, col: IDT) -> Tuple[ExecState, Optional[Province]]:
        """Add an province or update it if exists."""
        pass

    @abstractmethod
    def add_port(self, port: Port, col: IDT) -> Tuple[ExecState, Optional[Port]]:
        """Add a port or update it if exists"""
        pass

    @abstractmethod
    def add_tide(self, Tide, col: IDT) -> Tuple[ExecState, Optional[Tide]]:
        """Add a tide record"""
        pass

    @abstractmethod
    def get_area(self, area_id: str, col: IDT = None) -> Optional[Area]:
        """
        Get :class:`Area` by :param:`area_id`

        :param area_id: Id of :class:`Area`
        :param col: Compared column. It's required if col of :param:`area_id` is :col:`str`
        :return: :class:`Area` or :class:`None` if not found
        """
        pass

    @abstractmethod
    def get_province(self, province_id: str, col: IDT = None) -> Optional[Province]:
        """
        Get :class:`Province` by :param:`province_id`

        :param province_id: Id of :class:`Province`
        :param col: Compared column. It's required if col of :param:`province_id` is :col:`str`
        :return: :class:`Province` or :class:`None` if not found
        """
        pass

    @abstractmethod
    def get_port(self, port_id: str, col: IDT) -> Optional[Port]:
        """
        Get :class:`Port` by :param:`port_id`

        :param port_id: Id of :class:`Port`
        :param col: Compared column. It's required if col of :param:`port_id` is :col:`str`
        :return: :class:`Port` or :class:`None` if not found
        """
        pass

    @abstractmethod
    def get_tide(self, port_id: str, date: date, col: IDT) -> Optional[Tide]:
        """
        Get :class:`Tide` of specified date and port

        :param port_id: Id of :class:`Port`
        :param date: Specified date
        :param col: Compared column.
        :return: :class:`Tide` or :class:`None` if not found
        """
        pass

    @abstractmethod
    def get_areas(self) -> List[Area]:
        """Get all :class:`Area`s"""
        pass

    @abstractmethod
    def get_provinces(self, area: Union[Area, str], col: IDT) -> List[Province]:
        """
        Get all :class:`Province`s which area belongs.

        :param area: :class:`Area` instance or :prop:`area.id`
        :param col: Compared column. It's required if col of :param:`area` is :col:`str`
        """
        pass

    @abstractmethod
    def get_ports(self, province: Union[Province, str], col: IDT) -> List[Port]:
        """
        Get all :class:`Port`s which :param:`province` belongs.

        :param province: :class:`Province` instance or :prop:`province.id`
        :param col: Compared column. It's required if col of :param:`province` is :col:`str`
        """
        pass
