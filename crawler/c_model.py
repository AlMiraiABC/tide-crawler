"""Models for crawler"""
import datetime
from typing import Any, List, Optional, Tuple, Union

from db.dbutil import db_util
from db.model import Area, BaseClazz, Port, Tide, TideItem, WithInfo


class CBase(BaseClazz):
    def __init__(self, raw: Any) -> None:
        super().__init__()
        self._raw = raw

    @property
    def objectId(self) -> Optional[str]:
        pass

    @property
    def createdAt(self) -> Optional[datetime.datetime]:
        pass

    @property
    def updatedAt(self) -> Optional[datetime.datetime]:
        pass

    @property
    def raw(self) -> Optional[Any]:
        return self._raw

    @raw.setter
    def raw(self, data: Any):
        self.raw = data


class CWithInfo(CBase, WithInfo):
    def __init__(self, raw: Any, rid: str, name: str) -> None:
        super().__init__(raw)
        self._rid = rid
        self._name = name

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
    def __init__(self, raw: Any, rid: str, name: str) -> None:
        super().__init__(raw, rid, name)


class CPort(CWithInfo, Port):

    def __init__(self, raw: Any, rid: str, name: str, area: Union[Area, str], geopoint: Tuple[float, float]) -> None:
        super().__init__(raw, rid, name)
        self._area = db_util.get_area(area) if type(area) == str else area
        self._geopoint = geopoint

    @property
    def area(self) -> Optional[Area]:
        self._area

    @area.setter
    def area(self, area: Union[Area, str]):
        self._area = db_util.get_area(area) if type(area) == str else area

    @property
    def geopoint(self) -> Optional[Tuple[float, float]]:
        self._geopoint

    @geopoint.setter
    def geopoint(self, value: Tuple[float, float]):
        self._geopoint = value


class CTide(Tide, CBase):

    def __init__(self, raw: Any, day: List[TideItem], limit: List[TideItem], zone: str, datum: float, port: Union[Port, str], date: datetime.date = datetime.datetime.now().date) -> None:
        super.__init__(raw)
        self._day = day
        self._limit = limit
        self._zone = zone
        self._datum = datum
        self._port = db_util.get_port(port) if type(port) == str else port
        self._date = date

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
        return self.port

    @port.setter
    def port(self, value: Union[Port, str]):
        self.port = db_util.get_port(value) if type(value) == str else value

    @property
    def date(self) -> Optional[datetime.datetime]:
        return self.date

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
