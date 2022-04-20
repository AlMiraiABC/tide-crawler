
import asyncio
import json
import random
from datetime import datetime
from typing import List, Tuple

from storages.basedbutil import IDT, BaseDbUtil


class MockBaseClazz:
    objectId: str = None
    raw = None
    updatedAt: datetime = None
    createdAt: datetime = None


class MockWithInfo(MockBaseClazz):
    rid: str = None
    name: str = None


class MockArea(MockWithInfo):
    pass


class MockProvince(MockWithInfo):
    area: MockArea = None


class MockPort(MockWithInfo):
    province: MockProvince = None
    geopoint: Tuple[float, float] = None
    zone: str = None


def random_str(s='0123456789abcdef', l=24):
    """Generate a random string from :param:`s` with :param:`l` length."""
    return ''.join(random.choices(s, k=l))


def load_mock_data():
    with open('tests/cache/mock.json') as f:
        return json.load(f)


class MockDbUtil(BaseDbUtil):
    def __init__(self) -> None:
        self.data: List[dict] = load_mock_data()

    def __convert(self, a: MockWithInfo, o: dict):
        a.objectId = o['objectId']
        a.rid = o['rid']
        a.name = o['name']
        a.createdAt = datetime.fromisoformat(o['createdAt'])
        a.updatedAt = datetime.fromisoformat(o['updatedAt'])
        return a

    async def add_area(self, area, col: IDT):
        pass

    async def add_port(self, port, col: IDT):
        pass

    async def add_province(self, province, col: IDT):
        pass

    async def add_tide(self, tide, col: IDT):
        pass

    async def get_tide(self, port_id: str, d: datetime.date):
        pass

    async def open(self):
        pass

    async def close(self):
        pass

    async def get_area(self, area_id: str, col: IDT):
        for area in self.data:
            if area['objectId' if col == IDT.ID else 'rid'] == area_id:
                a = MockArea()
                return self.__convert(a, area)
        return None

    async def get_areas(self):
        return [self.__convert(MockArea(), area) for area in self.data]

    async def get_province(self, province_id: str, col: IDT):
        for area in self.data:
            for province in area.get('provinces', []):
                if province['objectId' if col == IDT.ID else 'rid'] == province_id:
                    p = MockProvince()
                    p.area = MockArea()
                    self.__convert(p.area, area)
                    return self.__convert(p, province)
        return None

    async def get_provinces(self, area, col: IDT = None):
        if type(area) == str:
            area_id = area
        else:
            area_id = area.objectId if col == IDT.ID else area.rid
        ret = []
        for area in self.data:
            if area['objectId' if col == IDT.ID else 'rid'] == area_id:
                for province in area.get('provinces', []):
                    p = MockProvince()
                    p.area = MockArea()
                    self.__convert(p.area, area)
                    ret.append(self.__convert(p, province))
        return ret

    async def get_port(self, port_id: str, col: IDT):
        for area in self.data:
            for province in area.get('provinces', []):
                for port in province.get('ports', []):
                    if port['objectId' if col == IDT.ID else 'rid'] == port_id:
                        p = MockPort()
                        p.province = MockProvince()
                        self.__convert(p.province, province)
                        return self.__convert(p, port)
        return None

    async def get_ports(self, province, col: IDT = None):
        if type(province) == str:
            province_id = province
        else:
            province_id = province.objectId if col == IDT.ID else province.rid
        ret = []
        for area in self.data:
            for province in area.get('provinces', []):
                if province['objectId' if col == IDT.ID else 'rid'] == province_id:
                    for port in province.get('ports', []):
                        p = MockPort()
                        p.province = MockProvince()
                        self.__convert(p.province, province)
                        ret.append(self.__convert(p, port))
        return ret
