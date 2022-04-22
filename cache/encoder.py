
from datetime import datetime
from json import JSONDecoder, JSONEncoder
from typing import Type, TypeVar
from storages.model import BaseClazz, WithInfo, Area, Province, Port
from crawlers.c_model import CArea, CProvince, CPort


_C = TypeVar('_C', bound=BaseClazz)
_W = TypeVar('_W', bound=WithInfo)


class BaseClazzEncoder(JSONEncoder):
    def default(self, o: BaseClazz) -> dict:
        d = {}
        d['objectId'] = o.objectId
        # datetime's type should be int, float or str
        d['createdAt'] = o.createdAt.isoformat() if o.createdAt else None
        d['updatedAt'] = o.updatedAt.isoformat() if o.updatedAt else None
        # remove origin because occured circular reference and ``o`` cannot be serialized.
        # d['origin'] = o
        return d


class BaseClazzDecoder(JSONDecoder):
    def __init__(self, c: Type[_C], *args, **kwargs):
        self.c = c
        JSONDecoder.__init__(
            self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, d: dict) -> _C:
        r = self.c()
        r.objectId = d.get('objectId')
        r.createdAt = datetime.fromisoformat(
            d['createdAt']) if d.get('createdAt') else None
        r.updatedAt = datetime.fromisoformat(
            d['updatedAt']) if d.get('updatedAt') else None
        return self.c()


class WithInfoEncoder(BaseClazzEncoder):
    def default(self, o: WithInfo) -> dict:
        d = super().default(o)
        d['rid'] = o.rid
        d['name'] = o.name
        return d


class WithInfoDecoder(BaseClazzDecoder):
    def __init__(self, c: Type[_W], *args, **kwargs):
        self.c = c
        super().__init__(
            self, c, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, d: dict) -> _W:
        r: WithInfo = super().object_hook(d)
        r.name = d.get('name')
        r.rid = d.get('rid')
        return r


class AreaEncoder(WithInfoEncoder):
    def default(self, o: Area) -> dict:
        d = super().default(o)
        d['provinces'] = {}
        return d


class AreaDecoder(WithInfoDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(self, CArea, *args, **kwargs)


class ProvinceEncoder(WithInfoEncoder):
    def default(self, o: Province) -> dict:
        d = super().default(o)
        d['ports'] = {}
        d['area'] = AreaEncoder().default(o.area) if o.area else None
        return d


class ProvinceDecoder(WithInfoDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(self, CProvince, *args, **kwargs)

    def object_hook(self, d: dict):
        r: Province = super().object_hook(d)
        r.area = AreaDecoder().object_hook(d['area']) if d.get(
            'area') else None
        return r


class PortEncoder(WithInfoEncoder):
    def default(self, o: Port) -> dict:
        d = super().default(o)
        d['zone'] = o.zone
        d['geopoint'] = o.geopoint
        d['province'] = ProvinceEncoder().default(
            o.province) if o.province else None
        return d


class PortDecoder(WithInfoDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(CPort, *args, **kwargs)

    def object_hook(self, d: dict):
        r: Port = super().object_hook(d)
        r.zone = d.get('zone')
        r.geopoint = d.get('geopoint')
        r.province = ProvinceDecoder().object_hook(
            d['province']) if d.get('province') else None
