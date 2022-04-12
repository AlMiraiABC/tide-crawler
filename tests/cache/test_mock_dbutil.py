import json
import random
from datetime import datetime
from typing import List
from unittest import TestCase

from storages.basedbutil import IDT
from tests.cache.mock_dbutil import MockDbUtil, MockWithInfo
from tests.storages.leancloud.test_lc_util import random_str


class TestMockDbUtil(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dbutil = MockDbUtil()
        with open('tests/util/mock.json') as f:
            cls.data: List[dict] = json.load(f)

    def assertWithInfo(self, a: MockWithInfo, b: dict):
        self.assertEquals(b['objectId'], a.objectId)
        self.assertEquals(b['rid'], a.rid)
        self.assertEquals(b['name'], a.name)
        self.assertEquals(datetime.fromisoformat(b['createdAt']), a.createdAt)
        self.assertEquals(datetime.fromisoformat(b['updatedAt']), a.updatedAt)

    def test_get_area(self):
        area_dict = random.choice(self.data)
        area = self.dbutil.get_area(area_dict['objectId'], IDT.ID)
        self.assertWithInfo(area, area_dict)

    def test_get_areas(self):
        ids = [a['objectId'] for a in self.data]
        areas = self.dbutil.get_areas()
        aids = [a.objectId for a in areas]
        self.assertListEqual(ids, aids)

    def test_get_area_unexist(self):
        ID = random_str()
        area = self.dbutil.get_area(ID, IDT.ID)
        self.assertIsNone(area)

    def test_get_province(self):
        province_dict = random.choice(self.data[0]['provinces'])
        province = self.dbutil.get_province(province_dict['objectId'], IDT.ID)
        self.assertWithInfo(province, province_dict)

    def test_get_provinces(self):
        area = self.data[0]
        ids = [p['objectId'] for p in area['provinces']]
        provinces = self.dbutil.get_provinces(area['objectId'], IDT.ID)
        pids = [p.objectId for p in provinces]
        self.assertListEqual(ids, pids)

    def test_get_provinces_area_unexist(self):
        ID = random_str()
        provinces = self.dbutil.get_provinces(ID)
        self.assertListEqual(provinces, [])

    def test_get_provinces_no_provinces(self):
        provinces = self.dbutil.get_provinces(
            self.data[-1]['objectId'], IDT.ID)
        self.assertListEqual(provinces, [])

    def test_get_port(self):
        province = self.data[0]['provinces'][0]
        port_dict = random.choice(province['ports'])
        port = self.dbutil.get_port(port_dict['objectId'], IDT.ID)
        self.assertWithInfo(port, port_dict)

    def test_get_ports(self):
        province = self.data[0]['provinces'][0]
        ids = [p['objectId'] for p in province['ports']]
        ports = self.dbutil.get_ports(province['objectId'], IDT.ID)
        pids = [p.objectId for p in ports]
        self.assertListEqual(ids, pids)

    def test_get_ports_province_unexist(self):
        ID = random_str()
        ports = self.dbutil.get_ports(ID, IDT.ID)
        self.assertListEqual(ports, [])

    def test_get_ports_no_ports(self):
        ports = self.dbutil.get_ports(
            self.data[0]['provinces'][-1]['objectId'], IDT.ID)
        self.assertListEqual(ports, [])
