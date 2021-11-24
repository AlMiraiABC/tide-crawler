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
    RID = 'Id'

    @property
    def rid(self) -> Optional[str]:
        return self.get(__WithInfo.RID)

    @rid.setter
    def cxbId(self, value: str):
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
    pass


class TideItem:
    TIME = 'time'
    HEIGHT = 'height'

    def __init__(self, time: datetime.datetime, height: float) -> None:
        self.time = time
        self.height = height


__TideItemDict = Dict[str, float]
__TideItemDicts = List[__TideItemDict]


class Tide(__BaseClazz):
    DAY = 'day'
    LIMIT = 'limit'
    PORT = 'port'
    DATE = 'date'

    @property
    def day(self) -> __TideItemDicts:
        return self.get(Tide.DAY)

    @day.setter
    def h24(self, value: __TideItemDicts):
        return self.set(Tide.DAY, value)

    @property
    def limit(self) -> __TideItemDicts:
        return self.get(Tide.LIMIT)

    @limit.setter
    def limit(self, value: __TideItemDicts):
        return self.set(Tide.LIMIT, value)

    @property
    def port(self) -> Port:
        return self.get(Tide.PORT)

    @port.setter
    def port(self, value: Port):
        return self.set(Tide.DISTRICT, value)

    @property
    def date(self):
        return self.get(Tide.DATE)

    @date.setter
    def date(self, value: str):
        return self.set(Tide.DATE, value)

    @staticmethod
    def to_dict(items: List[TideItem]) -> __TideItemDicts:
        return [item.__dict__ for item in items]

    @staticmethod
    def to_item(dicts: __TideItemDicts) -> List[TideItem]:
        return [Tide(d[TideItem.TIME], d[TideItem.HEIGHT]) for d in dicts]
