from typing import Iterable
from unittest import TestCase

from dao import *


def print_(info: Union[Iterable[object], object]):
    if not info:
        print(None)
        return
    if isinstance(info, Iterable):
        for e in info:
            print(e.__dict__ if e is not None else None)
        return
    print(info.__dict__)


class TestContinentDao(TestCase):

    def setUp(self) -> None:
        self.session = db_util.get_session()
        self.cd = ContinentDao(self.session)

    def tearDown(self) -> None:
        db_util.close_session(self.session)

    def test_get_all_continent(self):
        rs = self.cd.get_all_continent()
        print_(rs)
        self.assertIsNotNone(rs)

    def test_get_continent_exist(self):
        rs = self.cd.get_continent('亚洲')
        print_([rs])
        self.assertIsNotNone(rs)

    def test_get_continent_none(self):
        rs = self.cd.get_continent('澳大利亚')
        print_([rs])
        self.assertIsNone(rs)

    def test__get_continent_by_id(self):
        rs = self.cd._get_continent_by_id(7)
        print_([rs])
        self.assertIsNotNone(rs)

    def test__get_continent_by_name(self):
        rs = self.cd._get_continent_by_name('欧洲')
        print_([rs])
        self.assertIsNotNone(rs)

    def test__get_continent_by_class(self):
        rs = self.cd._get_continent_by_class(Continent(id=5))
        print_([rs])
        self.assertIsNotNone(rs)

    def test_insert(self):
        pass


class TestProvinceDao(TestCase):
    def setUp(self) -> None:
        self.session = db_util.get_session()
        self.pd = ProvinceDao(self.session)

    def tearDown(self) -> None:
        db_util.close_session(self.session)

    def test_get_province_exist(self):
        rs = self.pd.get_province('河北')
        print_([rs])
        self.assertIsNotNone(rs)

    def test_insert_success(self):
        p = Province(name='内蒙古')
        s, pi = self.pd.insert(p)
        print(s, pi.__dict__)

    def test_insert_exist(self):
        p = Province(name='河北')
        s, pi = self.pd.insert(p)
        print(s, pi.__dict__)

    def test__get_province_by_id(self):
        rs = self.pd._get_province_by_id(1)
        print_([rs])
        self.assertIsNotNone(rs)

    def test__get_province_by_name(self):
        rs = self.pd._get_province_by_name('河北')
        print_([rs])
        self.assertIsNotNone(rs)

    def test__get_province_by_class(self):
        pass

    def test_get_all_province(self):
        rs = self.pd.get_all_province()
        print_(rs)
        self.assertIsNotNone(rs)


class TestPortDao(TestCase):
    def setUp(self) -> None:
        self.session = db_util.get_session()
        self.pd = PortDao(self.session)

    def tearDown(self) -> None:
        db_util.close_session(self.session)

    def test__get_port_by_id(self):
        rs = self.pd._get_port_by_id(3)
        print_([rs])
        self.assertIsNotNone(rs)

    def test_get_ports_by_country_name(self):
        rs = self.pd.get_ports_by_country('中国')
        print_(rs)

    def test__get_port_by_class(self):
        pass

    def test__get_port_by_name(self):
        rs = self.pd._get_port_by_name('秦皇岛')
        print_([rs])
        self.assertIsNotNone(rs)

    def test_get_ports_by_province(self):
        rs = self.pd.get_ports_by_province('河北')
        print_(rs)
        self.assertIsNotNone(rs)

    def test_get_port(self):
        pass

    def test_get_ports_by_country(self):
        rs = self.pd.get_ports_by_country('中国')
        print_(rs)
        self.assertIsNotNone(rs)

    def test_insert_success(self):
        port = Port(name='葫芦岛', pid=108, country_id=1, latitude=88, longitude=32, datum=50, zone='-800')
        s, p = self.pd.insert(port)
        print(s, p.__dict__)


class TestChinaPortDao(TestCase):
    def setUp(self) -> None:
        self.session = db_util.get_session()
        self.cpd = ChinaPortDao(self.session)

    def tearDown(self) -> None:
        db_util.close_session(self.session)

    def test_insert_success(self):
        cp = ChinaPort(pid=6, province_id=1)
        s, c = self.cpd.insert(cp)
        print(s, c.__dict__)


class TestCountryDao(TestCase):
    def setUp(self) -> None:
        self.session = db_util.get_session()
        self.cd = CountryDao(self.session)

    def tearDown(self) -> None:
        db_util.close_session(self.session)

    def test__get_country_by_id(self):
        rs = self.cd._get_country_by_id(1)
        print_(rs)
        self.assertIsNotNone(rs)

    def test__get_country_by_name(self):
        rs = self.cd._get_country_by_name('中国')
        print_(rs)
        self.assertIsNotNone(rs)

    def test__get_country_by_class(self):
        pass

    def test_get_country(self):
        pass

    def test_get_country_by_continent(self):
        rs = self.cd.get_country_by_continent('亚洲')
        print_(rs)
        self.assertIsNotNone(rs)

    def test_insert(self):
        c = Country(name='澳大利亚', continent_id=4)
        s, ci = self.cd.insert(c)
        print_([s, ci])


class TestTideDao(TestCase):
    def setUp(self) -> None:
        self.session = db_util.get_session()
        self.td = TideDao(self.session)

    def tearDown(self) -> None:
        db_util.close_session(self.session)

    def test_get_tide_by_pid_and_date(self):
        self.fail()

    def test__exist(self):
        tide = Tide(pid=3,
                    t=datetime(2020, 9, 13, 8, 39, 59),
                    limit='[{"high": 36, "time": 20}, {"high": 32, "time": 21}]',
                    data='[{"high": 36, "time": 3}, {"high": 32, "time": 18}]')
        t = self.td._exist(tide)
        print_(t)

    def test_insert(self):
        tide = Tide(pid=5,
                    t=datetime(2020, 9, 13),
                    limit='[{"high": 36, "time": 20}, {"high": 32, "time": 21}]',
                    data='[{"high": 36, "time": 3}, {"high": 32, "time": 18}]')
        r, i = self.td.insert(tide)
        print(r, i.__dict__)
