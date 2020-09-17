from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

BaseTable = declarative_base()


class ChinaPort(BaseTable):
    __tablename__ = 'china_port'
    id = Column('id', Integer, primary_key=True)
    pid = Column('pid', Integer, ForeignKey('port.id'), unique=True)
    province_id = Column('province', Integer, ForeignKey('province.id'))
    port = relationship('Port')
    province = relationship('Province')

    def __repr__(self):
        return self.__dict__


class Continent(BaseTable):
    __tablename__ = 'continent'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(20), unique=True)
    countries = relationship('Country')

    def __repr__(self):
        return self.__dict__


class Country(BaseTable):
    __tablename__ = 'country'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(40), unique=True)
    continent_id = Column('continent', Integer, ForeignKey('continent.id'))
    ports = relationship('Port')


class Port(BaseTable):
    __tablename__ = 'port'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(40))
    pid = Column('pid', Integer, unique=True)
    country_id = Column('country', Integer, ForeignKey('country.id'))
    latitude = Column('latitude', Float)
    longitude = Column('longitude', Float)
    datum = Column('datum', Float)
    zone = Column('zone', String(10))
    china_port = relationship('ChinaPort')


class Province(BaseTable):
    __tablename__ = 'province'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(20), unique=True)
    ports = relationship('ChinaPort')
    china_port = relationship('ChinaPort')


class Tide(BaseTable):
    __tablename__ = 'tide'
    id = Column('id', Integer, primary_key=True)
    pid = Column('pid', Integer, ForeignKey('port.id'))
    t = Column('t', TIMESTAMP)
    data = Column('data', String)
    limit = Column('limit', String)
    port = relationship('Port')
