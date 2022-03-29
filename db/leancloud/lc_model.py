"""
class definitions for leancloud

See also
-------
https://leancloud.cn/docs/leanstorage_guide-python.html#hash23473483
"""

import datetime
from typing import Any, List, Optional, Union
from db.dbutil import db_util

from db.model import Area, BaseClazz, Port, Tide, TideItem, WithInfo

from leancloud import GeoPoint, Object


class LCBaseClazz(Object):
    OBJECT_ID = 'objectId'
    CREATED_AT = 'createdAt'
    UPDATED_AT = 'updatedAt'
    RAW = 'raw'

    def __init__(self, **attrs):
        super().__init__(**attrs, class_name=type(self).__name__)

    @property
    def objectId(self) -> Optional[str]:
        return self.get(LCBaseClazz.OBJECT_ID)

    @property
    def createdAt(self) -> Optional[datetime.datetime]:
        return self.get(LCBaseClazz.CREATED_AT)

    @property
    def updatedAt(self) -> Optional[datetime.datetime]:
        return self.get(LCBaseClazz.UPDATED_AT)

    @property
    def raw(self) -> Optional[Any]:
        return self.get(LCBaseClazz.RAW)

    @raw.setter
    def raw(self, data: Any):
        self.set(LCBaseClazz.RAW, data)


class LCWithInfo(LCBaseClazz):
    NAME = 'name'
    RID = 'rid'

    @property
    def rid(self) -> Optional[str]:
        return self.get(LCWithInfo.RID)

    @rid.setter
    def rid(self, value: str):
        self.set(LCWithInfo.RID, value)

    @property
    def name(self) -> Optional[str]:
        return self.get(LCWithInfo.NAME)

    @name.setter
    def name(self, value: str):
        self.set(LCWithInfo.NAME, value)


class LCArea(LCWithInfo):
    def __init__(self, **attrs):
        super().__init__(**attrs, class_name='Area')


class LCPort(LCWithInfo):
    AREA = 'area'
    GEOPOINT = 'geopoint'

    def __init__(self, **attrs):
        super().__init__(**attrs, class_name='Port')

    @property
    def area(self) -> LCArea:
        return self.get(LCPort.AREA)

    @area.setter
    def area(self, area: LCArea):
        self.set(LCPort.AREA, area)

    @property
    def geopoint(self) -> GeoPoint:
        return self.get(LCPort.GEOPOINT)

    @geopoint.setter
    def geopoint(self, value: GeoPoint):
        self.set(LCPort.GEOPOINT, value)


class LCTide(LCBaseClazz):
    DAY = 'day'
    LIMIT = 'limit'
    PORT = 'port'
    DATE = 'date'
    ZONE = 'zone'
    DATUM = 'datum'

    def __init__(self, **attrs):
        super().__init__(**attrs, class_name='Tide')

    def __to_tideitem(self, d: List[dict]):
        return [TideItem.from_dict(i) for i in d]

    def __to_dictlist(self, v: List[Union[TideItem, dict]]):
        return [i.to_dict() if type(i) == TideItem else i for i in v]

    @property
    def day(self) -> List[TideItem]:
        d: List[dict] = self.get(LCTide.DAY)
        return self.__to_tideitem(d)

    @day.setter
    def day(self, value: List[Union[TideItem, dict]]):
        self.set(LCTide.DAY, self.__to_dictlist(value))

    @property
    def limit(self) -> List[TideItem]:
        return self.__to_tideitem(self.get(LCTide.LIMIT))

    @limit.setter
    def limit(self, value: List[TideItem]):
        self.set(LCTide.LIMIT, self.__to_dictlist(value))

    @property
    def port(self) -> LCPort:
        return self.get(LCTide.PORT)

    @port.setter
    def port(self, value: Union[LCPort, str]):
        self.set(LCTide.PORT, value if type(value) ==
                 LCPort else db_util.get_port(value))

    @property
    def date(self) -> datetime.datetime:
        return self.get(LCTide.DATE)

    @date.setter
    def date(self, value: datetime.datetime):
        self.set(LCTide.DATE, value)

    @property
    def zone(self) -> str:
        return self.get(LCTide.ZONE)

    @zone.setter
    def zone(self, value: str):
        self.set(LCTide.LIMIT, value)

    @property
    def datum(self) -> float:
        return self.get(LCTide.DATUM)

    @datum.setter
    def datum(self, value: float):
        self.set(LCTide.DATUM, value)


BaseClazz.register(LCBaseClazz)
WithInfo.register(LCWithInfo)
Area.register(LCArea)
Port[GeoPoint].register(LCPort)
Tide.register(LCTide)
