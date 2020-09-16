from unittest import TestCase

from selector import Selector


class TestSelector(TestCase):
    def test_get_countries(self):
        Selector.get_countries('欧洲')

    def test_get_china_provinces(self):
        Selector.get_china_provinces()

    def test_get_other_countries_ports(self):
        Selector.get_other_countries_ports('美国')

    def test_get_china_province_ports(self):
        print(Selector.get_china_province_ports('河北'))

    def test_get_port_id(self):
        Selector.get_port_info('山海关')
