import json
import os
from json import JSONEncoder
from typing import List, Optional

from db.basedbutil import IDT, BaseDbUtil
from db.dbutil import DbUtil
from db.model import Area, BaseClazz, Port, Province, WithInfo

from util.validate import Value


class BaseClazzEncoder(JSONEncoder):
    def default(self, o: BaseClazz) -> dict:
        d = {}
        d['objectId'] = o.objectId
        # datetime's type should be int, float or str
        d['createdAt'] = o.createdAt.isoformat() if o.createdAt else None
        d['updatedAt'] = o.updatedAt.isoformat() if o.updatedAt else None
        d['origin'] = o
        return d


class WithInfoEncoder(BaseClazzEncoder):
    def default(self, o: WithInfo) -> dict:
        d = super().default(o)
        d['rid'] = o.rid
        d['name'] = o.name
        return d


class AreaEncoder(WithInfoEncoder):
    def default(self, o: Area) -> dict:
        d = super().default(o)
        d['provinces'] = {}
        return d


class ProvinceEncoder(WithInfoEncoder):
    def default(self, o: Province) -> dict:
        d = super().default(o)
        d['ports'] = {}
        d['area'] = o.area.objectId if o.area else None
        return d


class PortEncoder(WithInfoEncoder):
    def default(self, o: Port) -> dict:
        d = super().default(o)
        d['zone'] = o.zone
        d['geopoint'] = o.geopoint
        d['province'] = o.province.objectId if o.province else None
        return d


_PRE_ID = 'ID'
_PRE_RID = 'RID'


class CacheDB:
    """Cache util for db module."""

    # TODO: Consider using third-part local database, such as sqlite3
    def __init__(self, dump: str = 'cache.json', db_util: BaseDbUtil = None, *args, **kwargs) -> None:
        """
        :param dump: Dump json file name to load and save data.
        """
        self.cache_areas = {}  # cache, index areas
        self.cache_provinces = {}  # index provinces
        self.cache_ports = {}  # index ports
        self.db_util = db_util
        self.dargs = args
        self.dkwargs = kwargs
        if os.path.exists(dump):
            if not os.path.isfile(dump):
                raise ValueError(f'{dump} is not a file.')
        else:
            self.init_dump_file()
        self.dump_file_name = dump

    def init_dump_file(self):
        """
        Create a dump file with an empty json object.

        NOTE
        ------------
        This will clean all dump data.
        """
        with open(self.dump_file_name, *self.dargs, **self.dkwargs) as f:
            f.write('{}')

    def save(self):
        """Save caches to dump file."""
        with open('w', self.dump_file_name, encoding='utf-8') as f:
            json.dump(self.cache_areas, f)

    def load(self):
        """Load caches from dump file."""
        with open('r', self.dump_file_name, encoding='utf-8') as f:
            self.cache_areas = json.load(f)

    def __set_key(self, cache: dict, origin: WithInfo, value: dict):
        cache[_PRE_ID+origin.objectId] = value
        cache[_PRE_RID+origin.rid] = value

    def __del_key(self, cache: dict, origin: WithInfo):
        cache.pop(_PRE_ID+origin.objectId, None)
        cache.pop(_PRE_RID+origin.rid, None)

    def _add_area(self, area: Area):
        """Add :param:`area` in cache."""
        enc = AreaEncoder().default(area)
        self.__set_key(self.cache_areas, area, enc)

    def _rm_area(self, area: Area):
        """
        Remove :param:`area` from cache.
        Provinces and ports which belongs to this area will remove too.
        """
        for province in self.cache_areas[_PRE_ID+area.objectId]['provinces']:
            self._rm_province(province['origin'])
        self.__del_key(self.cache_areas, area)
        self.cache_areas.pop(_PRE_RID+area.rid, None)

    def _add_province(self, province: Province):
        """Add :param:`province` in cache."""
        enc = ProvinceEncoder().default(province)
        area = province.area
        provinces = self.cache_areas[_PRE_ID + area.objectId]['provinces']
        self.__set_key(provinces, province, enc)
        self.__set_key(self.cache_provinces, province, enc)

    def _rm_province(self, province: Province):
        area = province.area
        for port in self.cache_provinces[_PRE_ID+province.objectId]['ports']:
            self._rm_port(port['origin'])
        self.__del_key(self.cache_provinces, province)
        self.cache_areas[_PRE_ID +
                         area.objectId]['provinces'].pop(_PRE_ID+province.objectId, None)
        self.cache_areas[_PRE_RID+area.rid]['provinces'].pop(_PRE_ID+province)

    def _add_port(self, port: Port):
        enc = PortEncoder().default(port)
        province = port.province
        ports = self.cache_provinces[_PRE_ID + province.objectId]['ports']
        ports[_PRE_ID+port.objectId] = enc
        self.cache_provinces[_PRE_RID +
                             province.rid]['ports'][_PRE_RID+port.rid] = enc
        self.cache_ports[_PRE_ID+province.objectId] = enc
        self.cache_ports[_PRE_RID+province.rid] = enc

    def _rm_port(self, port: Port):
        pid = _PRE_ID+port.objectId
        prid = _PRE_RID+port.rid
        self.cache_ports.pop(pid, None)
        self.cache_ports.pop(prid, None)
        province = port.province
        ports = self.cache_provinces[_PRE_ID + province.objectId]['ports']
        ports.pop(pid, None)
        ports.pop(prid, None)

    def refresh_areas(self):
        """
        Re-fetch all areas data to cache.

        NOTE
        ----------
        It will clean all cache.
        """
        self.cache_areas.clear()
        self.cache_provinces.clear()
        self.cache_ports.clear()
        areas = DbUtil(self.db_util).get_areas()
        for area in areas:
            self._add_area(area)

    def refresh_provinces(self, area_id: Optional[str]):
        """
        Re-fetch provinces which belongs to :param:`area_id`.

        :param area_id:
            `Area.objectId`. It will get area from db if this area not found in cache.
            Or Set to ``None`` to refresh all provinces. Will not refresh areas.
        :raise ValueError: Set :param:`area_id`, but not cache it and not find from db.
        """
        def refresh(aid: str):
            ps = DbUtil(self.db_util).get_provinces(aid, col=IDT.ID)
            for p in ps:
                self._add_province(p)

        if Value.is_any_none_or_whitespace(area_id):
            self.cache_provinces.clear()
            self.cache_areas[_PRE_ID+aid]['provinces'].clear()
            # self.cache_areas[_PRE_RID+aid]['provinces'].clear()
            for aid in self.cache_areas.keys():
                refresh(aid)
        else:
            if area_id not in self.cache_areas.keys():
                area = DbUtil(self.db_util).get_area(area_id, IDT.ID)
                if area is None:
                    raise ValueError(f'area id {area_id} not found.')
                self._add_area(area)
            rmkeys = [k for k, v in self.cache_provinces.items()
                      if v['area'] == area_id]
            [self.cache_provinces.pop(k, None) for k in rmkeys]
            refresh(area_id)

    def refresh_ports(self, province_id: Optional[str]):
        """
        Re-fetch ports which belongs to :param:`province_id`.

        :param province_id:
            `Province.objectId`. It will get province from db if this province not found in cache.
            Or Set to ``None`` to refresh all ports. Will not refresh areas and provinces.
        :raise ValueError: Set :param:`province_id`, but not cache it and not find from db.
        """
        def refresh(pid: str):
            ps = DbUtil(self.db_util).get_ports(pid, col=IDT.ID)
            self.cache_provinces[pid]['ports'].clear()
            for p in ps:
                enc = PortEncoder().default(p)
                self.cache_provinces[pid]['ports'][p.objectId] = enc
                self.cache_ports.update({p.objectId: enc})

        if Value.is_any_none_or_whitespace(province_id):
            self.cache_ports.clear()
            for pid in self.cache_provinces.keys():
                refresh(pid)
        else:
            if province_id not in self.cache_provinces.keys():
                province = DbUtil(self.db_util).get_province(
                    province_id, IDT.ID)
                if province is None:
                    raise ValueError(f'province id {province_id} not found.')
                self.cache_provinces[province_id] = province
            refresh(province_id)

    def cmp_area(self, a1: Area, a2: Area) -> List[str]:
        """
        Compare two area instance.

        :return: Different attributes.
        """
        cmpn = self.__cmp_base(a1, a2)
        if not cmpn is None:
            return cmpn
        ret: list = []
        # optional objectId
        if not Value.is_any_none_or_whitespace(a1.objectId, a2.objectId):
            if a1.objectId != a2.objectId:
                ret.append('objectId')
        else:
            if a1.rid != a2.rid:
                ret.append('rid')
            if a1.name != a2.name:
                ret.append('name')
        return ret

    def __cmp_base(self, o1, o2) -> Optional[bool]:
        """
        Base comparison for None, type and id.

        :return:
            True if both are None or has equals id.
            False if one of None or difference type.
            None for other situations and continue to compare.
        """
        if o1 is None and o2 is None:
            return True
        if o1 is None or o2 is None:
            return False
        if type(o1) != type(o2):
            return False
        if id(o1) == id(o2):
            return True
        return None
