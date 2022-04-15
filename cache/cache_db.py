import json
import os
from json import JSONEncoder
from typing import List, Optional

from storages.basedbutil import IDT, BaseDbUtil, switch_idt
from storages.dbutil import DbUtil
from storages.model import Area, BaseClazz, Port, Province, WithInfo
from utils.singleton import singleton
from utils.validate import Value


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


@singleton
class CacheDB:
    """Cache storage for db module."""

    # HACK: Consider using third-part local database, such as sqlite3
    def __init__(self, dump: str = 'cache.json', db_util: BaseDbUtil = None, *args, **kwargs) -> None:
        """
        :param dump: Dump json file name to load and save data.
        :param db_util: Inner db util for :class:`DbUtil`
        """
        self.cache_areas = {}  # cache, index areas
        self.cache_provinces = {}  # index provinces
        self.cache_ports = {}  # index ports
        self.db_util = db_util
        self.dargs = args
        self.dkwargs = kwargs
        self.dump_file_name = dump
        if os.path.exists(dump):
            if not os.path.isfile(dump):
                raise ValueError(f'{dump} is not a file.')
        else:
            self.init_dump_file()
        self.load()

    def init_dump_file(self):
        """
        Create a dump file with an empty json object.

        NOTE
        ------------
        This will clean all dump data.
        """
        with open(self.dump_file_name, 'w', *self.dargs, **self.dkwargs) as f:
            f.write('{}')

    def save(self):
        """Save caches to dump file."""
        with open('w', self.dump_file_name, encoding='utf-8') as f:
            json.dump(self.cache_areas, f)

    def load(self):
        """Load caches from dump file."""
        # TODO: origin, convert dict to object
        with open(self.dump_file_name, 'r',  encoding='utf-8') as f:
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

    def get_area(self, area: str, col: IDT) -> Optional[Area]:
        """Get cached area."""
        area_dic = self._get_area_dict(area, col)
        return area_dic['origin'] if area_dic else None

    def __get_keys(self, caches: dict, key: str) -> list:
        return list({o[key] for o in caches.values()})

    def get_areas(self) -> List[Area]:
        return self.__get_keys(self.cache_areas, 'origin')

    def _get_area_dict(self, area: str, col: IDT) -> Optional[Area]:
        return switch_idt(col, lambda: self.cache_areas.get(_PRE_ID+area),
                          lambda: self.cache_areas.get(_PRE_RID+area))

    def get_province(self, province, col: IDT) -> Optional[Province]:
        """Get cached province."""
        province_dic = self._get_province_dict(province, col)
        return province_dic['origin'] if province_dic else None

    def _get_province_dict(self, province: str, col: IDT) -> Optional[Province]:
        return switch_idt(col, lambda: self.cache_provinces.get(_PRE_ID+province),
                          lambda: self.cache_provinces.get(_PRE_RID+province))

    def get_provinces(self, area: str, col: IDT) -> Optional[List[Province]]:
        area_dic = self._get_area_dict(area, col)
        return None if not area_dic else self.__get_keys(self.cache_provinces, 'origin')

    def get_port(self, port: str, col: IDT) -> Optional[Port]:
        """Get cached port."""
        port_dic = self._get_port_dict(port, col)
        return port_dic['origin'] if port_dic else None

    def get_ports(self, province: str, col: IDT) -> Optional[List[Port]]:
        province_dic = self._get_province_dict(province, col)
        return None if not province_dic else self.__get_keys(self.cache_provinces, 'origin')

    def _get_port_dict(self, port: str, col: IDT) -> Optional[Port]:
        return switch_idt(col, lambda: self.cache_ports.get(_PRE_ID+port),
                          lambda: self.cache_ports.get(_PRE_RID+port))

    async def refresh_areas(self):
        """
        Re-fetch all areas data to cache.

        NOTE
        ----------
        It will clean all cache.
        """
        self.cache_areas.clear()
        self.cache_provinces.clear()
        self.cache_ports.clear()
        areas = await DbUtil(self.db_util).get_areas()
        for area in areas:
            self._add_area(area)

    async def refresh_provinces(self, area_id: Optional[str]):
        """
        Re-fetch provinces which belongs to :param:`area_id`.

        :param area_id:
            `Area.objectId`. It will get area from db if this area not found in cache.
            Or Set to ``None`` to refresh all provinces. Will not refresh areas.
        :raise ValueError: Set :param:`area_id`, but not cache it and not find from db.
        """
        async def refresh(aid: str):
            ps = await DbUtil(self.db_util).get_provinces(aid, col=IDT.ID)
            for p in ps:
                self._add_province(p)

        if Value.is_any_none_or_whitespace(area_id):
            self.cache_provinces.clear()
            self.cache_areas[_PRE_ID+aid]['provinces'].clear()
            # self.cache_areas[_PRE_RID+aid]['provinces'].clear()
            for aid in self.cache_areas.keys():
                await refresh(aid)
        else:
            if _PRE_ID+area_id not in self.cache_areas.keys():
                area = await DbUtil(self.db_util).get_area(area_id, IDT.ID)
                if area is None:
                    raise ValueError(f'area id {area_id} not found.')
                self._add_area(area)
            rmkeys = [k for k, v in self.cache_provinces.items()
                      if v['area'] == area_id]
            [self.cache_provinces.pop(k, None) for k in rmkeys]
            await refresh(area_id)

    async def refresh_ports(self, province_id: Optional[str]):
        """
        Re-fetch ports which belongs to :param:`province_id`.

        :param province_id:
            `Province.objectId`. It will get province from db if this province not found in cache.
            Or Set to ``None`` to refresh all ports. Will not refresh areas and provinces.
        :raise ValueError: Set :param:`province_id`, but not cache it and not find from db.
        """
        async def refresh(pid: str):
            ps = await DbUtil(self.db_util).get_ports(pid, col=IDT.ID)
            self.cache_provinces[pid]['ports'].clear()
            for p in ps:
                enc = PortEncoder().default(p)
                self.cache_provinces[pid]['ports'][p.objectId] = enc
                self.cache_ports.update({p.objectId: enc})

        if Value.is_any_none_or_whitespace(province_id):
            self.cache_ports.clear()
            for pid in self.cache_provinces.keys():
                await refresh(pid)
        else:
            if _PRE_ID + province_id not in self.cache_provinces.keys():
                province = await DbUtil(self.db_util).get_province(
                    province_id, IDT.ID)
                if province is None:
                    raise ValueError(f'province id {province_id} not found.')
                self.cache_provinces[province_id] = province
            await refresh(province_id)
