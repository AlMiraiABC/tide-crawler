"""
table definitions for structured dataset
"""

from abc import ABC

from sqlalchemy import JSON, Column, Date, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

__BaseTable = declarative_base()


class BaseTable(__BaseTable, ABC):
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(20), unique=True)
    cxb_id = Column('cxb_id', Integer, nullable=True)
    create_time = Column('create_time', DateTime,
                         server_default="CURRENT_TIMESTAMP(3)")
    update_time = Column('update_time', DateTime, server_default="CURRENT_TIMESTAMP(3)",
                         server_onupdate="CURRENT_TIMESTAMP(3)")

    def __repr__(self):
        return self.__dict__


class Province(BaseTable):
    __tablename__ = 'province'
    cities = relationship('City', back_populates='province')


class City(BaseTable):
    __tablename__ = 'city'
    province_id = Column("province", Integer)
    province = relationship('Province', back_populates='cities')
    counties = relationship('County', back_populates='city')


class County(BaseTable):
    __tablename__ = 'county'
    city_id = Column('city', Integer)
    city = relationship('City', back_populates='counties')
    district = relationship('District', back_populates='county')


class District(BaseTable):
    """
    shouldn't get all tides through relationship, it is only clause by :class:`District.id`.
    Please use :method:`TideDao.get_tide_by_pid_and_date`.
    """
    __tablename__ = 'district'
    county_id = Column('county', Integer)
    county = relationship('County', back_populates='district')


class Tide(__BaseTable):
    __tablename__ = 'tide'
    id = Column('id', Integer, primary_key=True)
    h24 = Column('24h', JSON)
    limit = Column('limit', JSON)
    day = Column('day', Date)
    district_id = Column('district', Integer)
    district = relationship('District')
