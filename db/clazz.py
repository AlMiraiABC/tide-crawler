"""
class definitions for leancloud
"""

import datetime
from typing import Dict, List, Optional

import leancloud


class __BaseClazz(leancloud.Object):
    CLASS_NAME = __module__
    OBJECT_ID = 'objectId'
    CREATED_AT = 'createdAt'
    UPDATED_AT = 'updatedAt'

    @property
    def objectId(self) -> Optional[str]:
        return self.get(__BaseClazz.OBJECT_ID)

    @property
    def createdAt(self) -> Optional[datetime.datetime]:
        return self.get(__BaseClazz.CREATED_AT)

    @property
    def updatedAt(self) -> Optional[datetime.datetime]:
        return self.get(__BaseClazz.UPDATED_AT)


class __WithInfo(__BaseClazz):
    NAME = 'name'
    CXB_ID = 'cxbId'
    CNSS_ID = 'cnssId'

    @property
    def cxbId(self) -> Optional[str]:
        return self.get(__WithInfo.CXB_ID)

    @cxbId.setter
    def cxbId(self, value: str):
        return self.set(__WithInfo.CXB_ID, value)

    @property
    def cnssId(self) -> Optional[str]:
        return self.get(__WithInfo.CNSS_ID)

    @cnssId.setter
    def cnssId(self, value: str):
        return self.set(__WithInfo.CNSS_ID, value)

    @property
    def name(self) -> Optional[str]:
        return self.get(__WithInfo.NAME)

    @name.setter
    def name(self, value: str):
        return self.set(__WithInfo.NAME, value)


class Province(__WithInfo):
    pass


class City(__WithInfo):
    PROVINCE = 'province'

    @property
    def province(self) -> Province:
        return self.get(City.PROVINCE)

    @province.setter
    def province(self, value: Province):
        return self.set(City.PROVINCE, value)


class County(__WithInfo):
    CITY = 'city'

    @property
    def city(self) -> City:
        return self.get(County.CITY)

    @city.setter
    def city(self, value: City):
        return self.set(County.CITY, value)


class District(__WithInfo):
    COUNTY = 'county'

    @property
    def county(self) -> County:
        return self.get(District.COUNTY)

    @county.setter
    def county(self, value=County):
        return self.set(District.COUNTY, value)


class TideItem:
    TIME = 'time'
    HIGH = 'high'

    def __init__(self, time: datetime.datetime, high: float) -> None:
        self.time = time
        self.high = high


__TideItemDict = Dict[str, float]
__TideItemDicts = List[__TideItemDict]


class Tide(__BaseClazz):
    H24 = 'h24'
    LIMIT = 'limit'
    DISTRICT = 'district'

    @property
    def h24(self) -> __TideItemDicts:
        return self.get(Tide.H24)

    @h24.setter
    def h24(self, value: __TideItemDicts):
        return self.set(Tide.H24, value)

    @property
    def limit(self) -> __TideItemDicts:
        return self.get(Tide.LIMIT)

    @limit.setter
    def limit(self, value: __TideItemDicts):
        return self.set(Tide.LIMIT, value)

    @property
    def district(self) -> District:
        return self.get(Tide.DISTRICT)

    @district.setter
    def district(self, value: District):
        return self.set(Tide.DISTRICT, value)

    @staticmethod
    def to_dict(items: List[TideItem]) -> __TideItemDicts:
        return [item.__dict__ for item in items]

    @staticmethod
    def to_item(dicts: __TideItemDicts) -> List[TideItem]:
        return [Tide(d[TideItem.TIME], d[TideItem.HIGH]) for d in dicts]
