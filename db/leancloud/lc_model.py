"""
class definitions for leancloud

See also
-------
https://leancloud.cn/docs/leanstorage_guide-python.html#hash23473483
"""

import datetime
from typing import Any, List, Optional, Union

from db.model import Area, BaseClazz, Port, Province, Tide, TideItem, WithInfo

from leancloud import GeoPoint, Object


class LCBaseClazz(Object):
    OBJECT_ID = 'objectId'
    CREATED_AT = 'createdAt'
    UPDATED_AT = 'updatedAt'
    RAW = 'raw'

    def __init__(self):
        super().__init__()

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
    _class_name = 'Area'

    def __init__(self):
        super().__init__()
        self._class_name


class LCProvince(LCWithInfo):
    _class_name = ('Province')
    AREA = 'area'

    def __init__(self):
        super().__init__()

    @property
    def area(self) -> LCArea:
        return self.get(LCPort.AREA)

    @area.setter
    def area(self, area: LCArea):
        self.set(LCPort.AREA, area)


class LCPort(LCWithInfo):
    _class_name = 'Port'
    PROVINCE = 'province'
    GEOPOINT = 'geopoint'

    def __init__(self):
        super().__init__()

    @property
    def province(self) -> LCProvince:
        return self.get(LCPort.PROVINCE)

    @province.setter
    def province(self, province: LCProvince):
        self.set(LCPort.PROVINCE, province)

    @property
    def zone(self) -> str:
        return self.get(LCTide.ZONE)

    @zone.setter
    def zone(self, value: str):
        self.set(LCTide.LIMIT, value)

    @property
    def geopoint(self) -> GeoPoint:
        return self.get(LCPort.GEOPOINT)

    @geopoint.setter
    def geopoint(self, value: GeoPoint):
        self.set(LCPort.GEOPOINT, value)


class LCTide(LCBaseClazz):
    _class_name = 'Tide'
    DAY = 'day'
    LIMIT = 'limit'
    PORT = 'port'
    DATE = 'date'
    DATUM = 'datum'

    def __init__(self):
        super().__init__()

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
    def port(self, value: LCPort):
        self.set(LCTide.PORT, value)

    @property
    def date(self) -> datetime.datetime:
        return self.get(LCTide.DATE)

    @date.setter
    def date(self, value: datetime.datetime):
        self.set(LCTide.DATE, value)

    @property
    def datum(self) -> float:
        return self.get(LCTide.DATUM)

    @datum.setter
    def datum(self, value: float):
        self.set(LCTide.DATUM, value)


BaseClazz.register(LCBaseClazz)
WithInfo.register(LCWithInfo)
Area.register(LCArea)
Province.register(LCProvince)
Port[GeoPoint].register(LCPort)
Tide.register(LCTide)
