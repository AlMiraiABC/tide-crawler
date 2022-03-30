"""
base model class definitions
"""

import datetime
from abc import ABC, abstractmethod
from optparse import Option
from typing import Any, Generic, List, NewType, Optional, Tuple, TypeVar


class BaseClazz(ABC):
    """Base class. All of model classes implements it."""
    @property
    @abstractmethod
    def objectId(self) -> Optional[str]:
        """Row id. Generated automatically."""
        pass

    @property
    @abstractmethod
    def createdAt(self) -> Optional[datetime.datetime]:
        """Row created datetime. Generated automatically."""
        pass

    @property
    @abstractmethod
    def updatedAt(self) -> Optional[datetime.datetime]:
        """
        Row last updated datetime. Updated automactically.
        It is equals to :prop:`createdAt` when create.
        """
        pass

    @property
    @abstractmethod
    def raw(self) -> Optional[Any]:
        """
        Get crawled raw data.
        """
        pass

    @raw.setter
    @abstractmethod
    def raw(self, data: Any):
        """Set raw data from crawler."""
        pass


class WithInfo(BaseClazz, ABC):
    """Common information column definitions."""
    @property
    @abstractmethod
    def rid(self) -> Optional[str]:
        """Get crawled data id."""
        pass

    @rid.setter
    @abstractmethod
    def rid(self, value: str):
        """Set data id from crawler."""
        pass

    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        """Get name."""
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str):
        """Set name."""
        pass


class Area(WithInfo, ABC):
    """Area, Continent, Ocean, Sea"""
    pass


class Province(WithInfo, ABC):
    """Province information."""
    @property
    @abstractmethod
    def area(self) -> Optional[Area]:
        """Get related :class:`Area` belongs."""
        pass

    @area.setter
    @abstractmethod
    def area(self, area: Area):
        """Set related :class:`Area` belongs."""
        pass


# Generic type of GeoPoint
TGP = TypeVar('TGP')


class Port(WithInfo, Generic[TGP]):
    """Port infomations."""

    @property
    @abstractmethod
    def province(self) -> Optional[Province]:
        """Get related :class:`Province` belongs."""
        pass

    @province.setter
    @abstractmethod
    def province(self, province: Province):
        """Set related :class:`Province` belongs."""
        pass

    @property
    @abstractmethod
    def zone(self) -> Optional[str]:
        """Get port time zone."""
        pass

    @zone.setter
    @abstractmethod
    def zone(self, value: str):
        """Set port time zone."""
        pass

    @property
    @abstractmethod
    def geopoint(self) -> Optional[TGP]:
        """Get port coordinate."""
        pass

    @geopoint.setter
    @abstractmethod
    def geopoint(self, value: TGP):
        """Set port coordinate."""
        pass


class TideItem():
    """Store a tide data pair include time and height."""
    TIME = 'time'
    HEIGHT = 'height'

    def __init__(self, time: datetime.time, height: float) -> None:
        self.time = time
        self.height = height

    def to_dict(self) -> dict:
        """Convert self :class:`TideItem` to dict"""
        return {TideItem.TIME: str(self.time), TideItem.HEIGHT: self.height}

    @staticmethod
    def from_dict(value: dict):
        """Convert dict to :class:`TideItem`"""
        time = datetime.time.fromisoformat(value[TideItem.TIME])
        height = value[TideItem.HEIGHT]
        return TideItem(time, height)


class Tide(BaseClazz):
    """Tide data of one day."""

    @property
    @abstractmethod
    def day(self) -> Optional[List[TideItem]]:
        """Get 24 hours tide data."""
        pass

    @day.setter
    @abstractmethod
    def day(self, value: List[TideItem]):
        """Set 24 hours tide data."""
        pass

    @property
    @abstractmethod
    def limit(self) -> Optional[List[TideItem]]:
        """Get tide limitations."""
        pass

    @limit.setter
    @abstractmethod
    def limit(self, value: List[TideItem]):
        """Set tide limitations."""
        pass

    @property
    @abstractmethod
    def port(self) -> Optional[Port]:
        """Get tide data related :class:`Port` belongs."""
        pass

    @port.setter
    @abstractmethod
    def port(self, value: Port):
        """Set tide data related :class:`Port` belongs."""
        pass

    @property
    @abstractmethod
    def date(self) -> Optional[datetime.datetime]:
        """Get tide data created datetime."""
        pass

    @date.setter
    @abstractmethod
    def date(self, value: datetime.datetime):
        """Set tide date created datetime."""
        pass

    @property
    @abstractmethod
    def datum(self) -> Optional[float]:
        """Get tide height datum plane(cm)."""
        pass

    @datum.setter
    @abstractmethod
    def datum(self, value: float):
        """Set tide height datum plane(cm)."""
        pass
