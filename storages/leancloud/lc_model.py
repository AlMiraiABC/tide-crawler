"""
class definitions for leancloud

See also
-------
https://leancloud.cn/docs/leanstorage_guide-python.html#hash23473483
"""

import datetime
from typing import Any, List, Optional, Tuple, Type, Union

from storages.model import Area, BaseClazz, Port, Province, Tide, TideItem, TideItemDict, WithInfo

from leancloud import GeoPoint, Object

from utils.meta import merge_meta


class LCBaseClazz(merge_meta(Object, BaseClazz)):
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

    def get_rel(self, key: str, c: Type[Object]):
        o: Object = self.get(key)
        if isinstance(o, c):
            return o
        if o and o.id:
            lco = c.query.get(o.id)
            if lco.is_existed():
                return lco
        return None


class LCWithInfo(LCBaseClazz, WithInfo):
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


@Object.as_class("Area")
class LCArea(LCWithInfo, Area):
    def __init__(self):
        super().__init__()


@Object.as_class("Province")
class LCProvince(LCWithInfo, Province):
    AREA = 'area'

    def __init__(self):
        super().__init__()

    @property
    def area(self) -> LCArea:
        return self.get_rel(LCProvince.AREA, LCArea)

    @area.setter
    def area(self, area: LCArea):
        self.set(LCProvince.AREA, area)


@Object.as_class("Port")
class LCPort(LCWithInfo, Port):
    PROVINCE = 'province'
    GEOPOINT = 'geopoint'
    ZONE = 'zone'

    def __init__(self):
        super().__init__()

    @property
    def province(self) -> LCProvince:
        return self.get_rel(LCPort.PROVINCE, LCProvince)

    @province.setter
    def province(self, province: LCProvince):
        self.set(LCPort.PROVINCE, province)

    @property
    def zone(self) -> str:
        return self.get(LCPort.ZONE)

    @zone.setter
    def zone(self, value: str):
        self.set(LCPort.ZONE, value)

    @property
    def geopoint(self) -> Tuple[float, float]:
        gp: GeoPoint = self.get(LCPort.GEOPOINT)
        return (gp.latitude, gp.longitude) if gp else None

    @geopoint.setter
    def geopoint(self, value: Tuple[float, float]):
        self.set(LCPort.GEOPOINT, GeoPoint(value[0], value[1]))


@Object.as_class("Tide")
class LCTide(LCBaseClazz, Tide):
    DAY = 'day'
    LIMIT = 'limit'
    PORT = 'port'
    DATE = 'date'
    DATUM = 'datum'

    def __init__(self):
        super().__init__()

    def __to_tideitems(self, d: List[dict]):
        return [TideItem.from_dict(i) for i in d]

    def __to_dicts(self, v: List[Union[TideItem, TideItemDict]]):
        return [i.to_dict() if type(i) == TideItem else i for i in v]

    @property
    def day(self) -> List[TideItem]:
        d: List[dict] = self.get(LCTide.DAY)
        return self.__to_tideitems(d)

    @day.setter
    def day(self, value: List[Union[TideItem, TideItemDict]]):
        self.set(LCTide.DAY, self.__to_dicts(value))

    @property
    def limit(self) -> List[TideItem]:
        return self.__to_tideitems(self.get(LCTide.LIMIT))

    @limit.setter
    def limit(self, value: List[TideItem]):
        self.set(LCTide.LIMIT, self.__to_dicts(value))

    @property
    def port(self) -> LCPort:
        return self.get_rel(LCTide.PORT, LCPort)

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
