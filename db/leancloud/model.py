"""
class definitions for leancloud

See also
-------
https://leancloud.cn/docs/leanstorage_guide-python.html#hash23473483
"""

import datetime
from typing import Any, Dict, List, Optional, Union

import leancloud


class __BaseClazz(leancloud.Object):
    CLASS_NAME = __module__
    OBJECT_ID = 'objectId'
    CREATED_AT = 'createdAt'
    UPDATED_AT = 'updatedAt'
    RAW = 'raw'

    @property
    def objectId(self) -> Optional[str]:
        return self.get(__BaseClazz.OBJECT_ID)

    @property
    def createdAt(self) -> Optional[datetime.datetime]:
        return self.get(__BaseClazz.CREATED_AT)

    @property
    def updatedAt(self) -> Optional[datetime.datetime]:
        return self.get(__BaseClazz.UPDATED_AT)

    @property
    def raw(self) -> Optional[Dict[str, Any]]:
        return self.get(__BaseClazz.RAW)

    @raw.setter
    def raw(self, data: Union[Dict[str, Any], str]):
        return self.set(__BaseClazz.RAW, data)


class __WithInfo(__BaseClazz):
    NAME = 'name'
    RID = 'RId'

    @property
    def rid(self) -> Optional[str]:
        return self.get(__WithInfo.RID)

    @rid.setter
    def rid(self, value: str):
        return self.set(__WithInfo.RID, value)

    @property
    def name(self) -> Optional[str]:
        return self.get(__WithInfo.NAME)

    @name.setter
    def name(self, value: str):
        return self.set(__WithInfo.NAME, value)


class Area(__WithInfo):
    pass


class Port(__WithInfo):
    AREA = 'area'
    LATITUDE = 'latitude'
    LONGITUDE = 'longitude'

    @property
    def area(self) -> Area:
        return self.get(Port.AREA)

    @area.setter
    def area(self, area: Area):
        return self.set(Port.AREA, area)

    @property
    def latitude(self) -> float:
        return self.get(Port.LATITUDE)

    @latitude.setter
    def latitude(self, value: float):
        return self.set(Port.LATITUDE, value)

    @property
    def longitude(self) -> float:
        return self.get(Port.LONGITUDE)

    @longitude.setter
    def longitude(self, value: float):
        return self.set(Port.LONGITUDE, value)


class TideItem:
    TIME = 'time'
    HEIGHT = 'height'

    def __init__(self, time: datetime.time, height: float) -> None:
        self.time = time
        self.height = height


class Tide(__BaseClazz):
    DAY = 'day'
    LIMIT = 'limit'
    PORT = 'port'
    DATE = 'date'
    ZONE = 'zone'
    DATUM = 'datum'

    @property
    def day(self) -> List[Dict[str, float]]:
        return self.get(Tide.DAY)

    @day.setter
    def day(self, value: List[Dict[str, float]]):
        return self.set(Tide.DAY, value)

    @property
    def limit(self) -> List[Dict[str, float]]:
        return self.get(Tide.LIMIT)

    @limit.setter
    def limit(self, value: List[Dict[str, float]]):
        return self.set(Tide.LIMIT, value)

    @property
    def port(self) -> Port:
        return self.get(Tide.PORT)

    @port.setter
    def port(self, value: Port):
        return self.set(Tide.PORT, value)

    @property
    def date(self) -> datetime.datetime:
        return self.get(Tide.DATE)

    @date.setter
    def date(self, value: datetime.datetime):
        return self.set(Tide.DATE, value)

    @property
    def zone(self) -> str:
        return self.get(Tide.ZONE)

    @zone.setter
    def zone(self, value: str):
        return self.set(Tide.LIMIT, value)

    @property
    def datum(self) -> float:
        return self.get(Tide.DATUM)

    @datum.setter
    def datum(self, value: float):
        return self.set(Tide.DATUM, value)

    @staticmethod
    def to_dict(items: List[TideItem]) -> List[Dict[str, float]]:
        return [item.__dict__ for item in items]

    @staticmethod
    def to_item(dicts: List[Dict[str, float]]) -> List[TideItem]:
        return [Tide(d[TideItem.TIME], d[TideItem.HEIGHT]) for d in dicts]
