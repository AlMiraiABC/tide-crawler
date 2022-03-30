"""
table definitions for structured dataset
"""

import datetime
from typing import Any, List, NewType, Optional, Tuple, Union
from unicodedata import name

from db import dbutil
from db.model import Area, BaseClazz, Port, Province, Tide, TideItem, WithInfo
from sqlalchemy import (JSON, Column, Date, DateTime, Float, ForeignKey,
                        Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

__BaseTable = declarative_base()


class RDBBaseClazz(__BaseTable, BaseClazz):
    cid = Column('id', Integer, primary_key=True)
    ccreatedAt = Column('createdAt', DateTime,
                        server_default="CURRENT_TIMESTAMP(3)")
    cupdatedAt = Column('updatedAt', DateTime, server_default="CURRENT_TIMESTAMP(3)",
                        server_onupdate="CURRENT_TIMESTAMP(3)")
    draw = Column('raw', JSON)

    @property
    def objectId(self) -> Optional[str]:
        return self.cid

    @property
    def createdAt(self) -> Optional[datetime.datetime]:
        return self.ccreatedAt

    @property
    def updatedAt(self) -> Optional[datetime.datetime]:
        return self.cupdatedAt

    @property
    def raw(self) -> Optional[Any]:
        return self.draw

    @raw.setter
    def raw(self, data: Any):
        self.draw = data

    def __repr__(self):
        return self.__dict__


class RDBWithInfo(RDBBaseClazz, WithInfo):
    dname = Column('name', String)
    drid = Column('rid', String)

    @property
    def rid(self) -> Optional[str]:
        return self.rid

    @rid.setter
    def rid(self, value: str):
        self.rid = value

    @property
    def name(self) -> Optional[str]:
        return name

    @name.setter
    def name(self, value: str):
        self.name = value


class RDBArea(RDBWithInfo, Area):
    __tablename__ = 'area'
    dprovinces = relationship('RDBProvince', back_populates='darea')


class RDBProvince(RDBWithInfo, Province):
    __tablename__ = 'province'
    darea_id = Column(Integer, ForeignKey('area.id'))
    darea = relationship('RDBArea', back_populates='dprovinces')
    dports = relationship('RDBPort', back_populates='dprovince')

    @property
    def area(self) -> RDBArea:
        return self.darea

    @area.setter
    def area(self, area: RDBArea):
        self.darea = area


# (latigude, longitude)
GeoPoint = NewType('GeoPoint', Tuple[float, float])


class RDBPort(RDBWithInfo, Port[GeoPoint]):
    __tablename__ = 'port'
    dzone = Column('zone', String)
    dlat = Column('lat', Float)
    dlon = Column('lon', Float)
    dprovince_id = Column('province_id'. Integer, ForeignKey('province.id'))
    dprovince = relationship('RDBProvince', back_populates='dports')

    @property
    def province(self) -> RDBProvince:
        return self.dprovince

    @province.setter
    def province(self, province: RDBProvince):
        self.dprovince = province

    @property
    def zone(self) -> str:
        return self.dzone

    @zone.setter
    def zone(self, value: str):
        self.dzone = value

    @property
    def geopoint(self) -> GeoPoint:
        return (self.dlat, self.dlon)

    @geopoint.setter
    def geopoint(self, value: GeoPoint):
        self.dlat = value[0]
        self.dlon = value[1]


class RDBTide(RDBBaseClazz, Tide):
    __tablename__ = 'tide'
    dlimit = Column('limit', JSON)
    dday = Column('day', JSON)
    dport_id = Column('port_id', Integer, ForeignKey('port.id'))
    dport = relationship('Port')
    ddate = Column('date', Date)
    ddatum = Column('datum', Float)

    def __to_tideitem(self, d: List[dict]):
        return [TideItem.from_dict(i) for i in d]

    def __to_dictlist(self, v: List[Union[TideItem, dict]]):
        return [i.to_dict() if type(i) == TideItem else i for i in v]

    @property
    def day(self) -> List[TideItem]:
        d: List[dict] = self.dday
        return self.__to_tideitem(d)

    @day.setter
    def day(self, value: List[Union[TideItem, dict]]):
        self.dday = self.__to_dictlist(value)

    @property
    def limit(self) -> List[TideItem]:
        return self.__to_tideitem(self.dlimit)

    @limit.setter
    def limit(self, value: List[TideItem]):
        self.dlimit = self.__to_dictlist(value)

    @property
    def port(self) -> RDBPort:
        return self.dport

    @port.setter
    def port(self, value: Union[RDBPort, str]):
        self.dport = value if type(
            value) == RDBPort else dbutil.get_port(value)

    @property
    def date(self) -> datetime.datetime:
        return self.ddate

    @date.setter
    def date(self, value: datetime.datetime):
        self.ddate = value

    @property
    def datum(self) -> float:
        return self.ddate

    @datum.setter
    def datum(self, value: float):
        self.ddatum = value
