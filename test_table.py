from typing import List, Union, Iterable
from unittest import TestCase

from backend.table import *
from util.db import DbUtil

db_util = DbUtil()


class TestTable(TestCase):
    def test_china_port_query(self):
        """测试china_port表查询本表字段"""
        session = db_util.get_session()
        rs: List[ChinaPort] = session.query(ChinaPort).filter(ChinaPort.province_id == 2).all()
        print_(rs)
        print(rs[0].province.__dict__)
        print(rs[0].port.__dict__)

    def test_continent_query(self):
        session = db_util.get_session()
        rs: Continent = session.query(Continent).filter(Continent.name == '亚洲').first()
        print(rs.__dict__)
        print_(rs.countries)

    def test_country_query(self):
        session = db_util.get_session()
        rs: Country = session.query(Country).filter(Country.id == 1).first()
        print(rs.__dict__)
        print_(rs.ports)

    def test_province_query(self):
        session = db_util.get_session()
        rs: Province = session.query(Province).filter(Province.id == 2).first()
        print(rs.__dict__)
        print_(rs.ports)

    def test_tide_query(self):
        session = db_util.get_session()
        rs: Tide = session.query(Tide).filter(Tide.id == 3).first()
        print(rs.__dict__)
        print(rs.port.__dict__)


def print_(info: Union[Iterable[object], object]):
    if not info:
        print(None)
        return
    if isinstance(info, Iterable):
        for e in info:
            print(e.__dict__ if e is not None else None)
        return
    print(info.__dict__)
