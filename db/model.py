"""
base model class definitions
"""

import datetime
from abc import ABC, abstractmethod
from typing import Any, Generic, List, NewType, Optional, Tuple, TypeVar


class BaseClazz(ABC):
    """Base class, all of model classes implements it."""
    @property
    @abstractmethod
    def objectId(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def createdAt(self) -> Optional[datetime.datetime]:
        pass

    @property
    @abstractmethod
    def updatedAt(self) -> Optional[datetime.datetime]:
        pass

    @property
    @abstractmethod
    def raw(self) -> Optional[Any]:
        pass

    @raw.setter
    @abstractmethod
    def raw(self, data: Any):
        pass


class WithInfo(BaseClazz, ABC):
    @property
    @abstractmethod
    def rid(self) -> Optional[str]:
        pass

    @rid.setter
    @abstractmethod
    def rid(self, value: str):
        pass

    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str):
        pass


class Area(WithInfo, ABC):
    pass


# (latigude, longitude)
GeoPoint = NewType('GeoPoint', Tuple[float, float])

TGP = TypeVar('TGP')


class Port(WithInfo, Generic[TGP]):

    @property
    @abstractmethod
    def area(self) -> Optional[Area]:
        pass

    @area.setter
    @abstractmethod
    def area(self, area: Area):
        pass

    @property
    @abstractmethod
    def geopoint(self) -> Optional[TGP]:
        pass

    @geopoint.setter
    @abstractmethod
    def geopoint(self, value: TGP):
        pass


class TideItem():
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
    @property
    @abstractmethod
    def day(self) -> Optional[List[TideItem]]:
        pass

    @day.setter
    @abstractmethod
    def day(self, value: List[TideItem]):
        pass

    @property
    @abstractmethod
    def limit(self) -> Optional[List[TideItem]]:
        pass

    @limit.setter
    @abstractmethod
    def limit(self, value: List[TideItem]):
        pass

    @property
    @abstractmethod
    def port(self) -> Optional[Port]:
        pass

    @port.setter
    @abstractmethod
    def port(self, value: Port):
        pass

    @property
    @abstractmethod
    def date(self) -> Optional[datetime.datetime]:
        pass

    @date.setter
    @abstractmethod
    def date(self, value: datetime.datetime):
        pass

    @property
    @abstractmethod
    def zone(self) -> Optional[str]:
        pass

    @zone.setter
    @abstractmethod
    def zone(self, value: str):
        pass

    @property
    @abstractmethod
    def datum(self) -> Optional[float]:
        pass

    @datum.setter
    @abstractmethod
    def datum(self, value: float):
        pass
