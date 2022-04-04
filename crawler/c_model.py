"""Models for crawler"""
import datetime
from typing import Any, List, Optional, Tuple

from db.model import Area, BaseClazz, Port, Province, Tide, TideItem, WithInfo


class CBase(BaseClazz):
    def __init__(self) -> None:
        super().__init__()
        self._raw = None
        self._created_at = datetime.datetime.now()
        self._updated_at = datetime.datetime.now()

    @property
    def objectId(self) -> Optional[str]:
        return None

    @property
    def createdAt(self) -> Optional[datetime.datetime]:
        return self._created_at

    @property
    def updatedAt(self) -> Optional[datetime.datetime]:
        return self._updated_at

    @property
    def raw(self) -> Optional[Any]:
        return self._raw

    @raw.setter
    def raw(self, data: Any):
        self._raw = data


class CWithInfo(CBase, WithInfo):
    def __init__(self) -> None:
        super().__init__()
        self._rid: str = None
        self._name: str = None

    @property
    def rid(self) -> Optional[str]:
        return self.rid

    @rid.setter
    def rid(self, value: str):
        self.rid = value

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value


class CArea(CWithInfo, Area):
    def __init__(self) -> None:
        super().__init__()


class CProvince(CWithInfo, Province):
    def __init__(self) -> None:
        super().__init__()
        self._area: Area = None

    @property
    def area(self) -> Optional[Area]:
        return self._area

    @area.setter
    def area(self, value: Area):
        self._area = value


class CPort(CWithInfo, Port):

    def __init__(self) -> None:
        super().__init__()
        self._province: Province = None
        self._geopoint: Tuple[float, float] = None
        self._zone: str = None

    @property
    def province(self) -> Optional[Province]:
        self._province

    @province.setter
    def province(self, value: Province):
        self._province = value

    @property
    def geopoint(self) -> Optional[Tuple[float, float]]:
        self._geopoint

    @geopoint.setter
    def geopoint(self, value: Tuple[float, float]):
        self._geopoint = value


class CTide(Tide, CBase):

    def __init__(self) -> None:
        super().__init__()
        self._day: List[TideItem] = []
        self._limit: List[TideItem] = []
        self._datum: float = None
        self._port: Port = None
        self._date: datetime.date = datetime.datetime.now()

    @property
    def day(self) -> Optional[List[TideItem]]:
        return self._day

    @day.setter
    def day(self, value: List[TideItem]):
        self._day = value

    @property
    def limit(self) -> Optional[List[TideItem]]:
        return self._limit

    @limit.setter
    def limit(self, value: List[TideItem]):
        self._limit = value

    @property
    def port(self) -> Optional[Port]:
        return self._port

    @port.setter
    def port(self, value: Port):
        self._port = value

    @property
    def date(self) -> Optional[datetime.datetime]:
        return self._date

    @date.setter
    def date(self, value: datetime.datetime):
        self._date = value

    @property
    def zone(self) -> Optional[str]:
        return self._zone

    @zone.setter
    def zone(self, value: str):
        self._zone = value

    @property
    def datum(self) -> Optional[float]:
        return self._datum

    @datum.setter
    def datum(self, value: float):
        self._datum = value
