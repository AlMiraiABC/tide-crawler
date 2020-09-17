from abc import abstractmethod, ABC
from datetime import datetime
from time import struct_time
from typing import List, Union, Optional, Tuple, TypeVar, Generic

from sqlalchemy.orm import Session

from backend.table import *
from util.db import db_util, ExecState
from util.validate import Value

_ValueErrorInfo = 'None or Empty values: '
_TypeErrorInfo = 'Type Error: '

_Dao = TypeVar('_Dao')


class BaseDao(Generic[_Dao]):
    def __init__(self, session: Session):
        self.session = session

    def insert(self, record: _Dao) -> Tuple[ExecState, _Dao]:
        """
        当数据库中未找到(根据self._exist()判断)时插入该省份信息

        :return: 执行结果, 数据库内的信息
        """
        r = self._exist(record)
        if r:
            return ExecState.EXIST, r
        return self._insert(record), record

    @abstractmethod
    def _exist(self, record: _Dao) -> _Dao:
        """
        :return: T if exist or else None
        """
        pass

    def _insert(self, entity: BaseTable) -> ExecState:
        # noinspection PyBroadException
        try:
            self.session.add(entity)
            return ExecState.SUCCESS
        except Exception:
            return ExecState.FAIL


class ProvinceDao(BaseDao[Province], ABC):

    def get_all_province(self) -> List[Province]:
        """
        获得所有省份(:class:`Province`)

        :return: 所有大洲
        """
        provinces = self.session.query(_Dao).all()
        return provinces

    def get_province(self, province: Union[int, str, Province]) -> Optional[_Dao]:
        """
        根据 ``Province.id`` or ``Province.name`` or ``Province`` 获得 :class:`Province`

        :param province: Province.id or Province.name or Province.
            若类型为Continent，则使用 id 属性查找, 若 id 不可用则使用 name 属性查找
        :return: Province if exist or else None
        """
        if not province:
            return None
        if type(province) == int:
            return self._get_province_by_id(province)
        elif type(province) == str:
            return self._get_province_by_name(province)
        elif type(province) == Province:
            return self._get_province_by_class(province)
        raise TypeError(f'{_TypeErrorInfo}[province]')

    def _get_province_by_id(self, p_id: int) -> Optional[Province]:
        """根据 ``Province.id`` 获得 :class:`Province`"""
        if p_id:
            p = self.session.query(Province).get(p_id)
            return p
        return None

    def _get_province_by_name(self, p_name: str) -> Optional[Province]:
        """根据 ``Province.name`` 获得 :class:`Province`"""
        if p_name:
            p = self.session.query(Province).filter(Province.name == p_name).first()
            return p
        return None

    def _get_province_by_class(self, p: Province) -> Optional[Province]:
        """使用 ``p.id`` 查找, 若 ``p.id`` 不可用则使用 ``p.name`` """
        if p:
            if p.id:
                return self._get_province_by_id(p.id)
            elif p.name:
                return self._get_province_by_name(p.name)
        return None

    def _exist(self, record: Province) -> Province:
        """
        当数据库中是否存在(:prop:`province.name`)
        """
        if Value.is_any_none_or_empty([record, record.name]):
            raise ValueError(f'{_ValueErrorInfo}[province, province.name]')
        r = self.session.query(_Dao) \
            .filter(Continent.name == record.name) \
            .first()
        return r


class ContinentDao(BaseDao[Continent], ABC):

    def get_all_continent(self) -> List[Continent]:
        """
        获得所有大洲(:class:`Continent`)

        :return: 所有大洲
        """
        continents = self.session.query(Continent).all()
        return continents

    def get_continent(self, continent: Union[int, str, Continent]) -> Optional[Continent]:
        """
        根据 ``Continent.id`` or ``Continent.name`` or ``Continent`` 获得 :class:`Continent`

        :param continent: Continent.id or Continent.name or Continent.
            若类型为Continent，则使用 id 属性 查找, 若 id 不可用则使用 name 属性查找
        :return: Continent if exist or else None
        """
        if not continent:
            return None
        if type(continent) == int:
            return self._get_continent_by_id(continent)
        elif type(continent) == str:
            return self._get_continent_by_name(continent)
        elif type(continent) == _Dao:
            return self._get_continent_by_class(continent)
        raise TypeError(f'{_TypeErrorInfo}[continent]')

    def _get_continent_by_id(self, c_id: int) -> Optional[Continent]:
        """根据 ``Continent.id`` 获得 :class:`Continent`"""
        if c_id:
            c = self.session.query(Continent).get(c_id)
            return c
        return None

    def _get_continent_by_name(self, c_name: str) -> Optional[Continent]:
        """根据 ``Continent.name`` 获得 :class:`Continent`"""
        if c_name:
            c = self.session.query(Continent) \
                .filter(Continent.name == c_name) \
                .first()
            return c
        return None

    def _get_continent_by_class(self, c: Continent) -> Optional[Continent]:
        """使用 ``c.id`` 查找, 若 ``c.id`` 不可用则使用 ``c.name`` """
        if c:
            if c.id:
                return self._get_continent_by_id(c.id)
            elif c.name:
                return self._get_continent_by_name(c.name)
        return None

    def _exist(self, record: Continent) -> Continent:
        if Value.is_any_none_or_empty([record, record.name]):
            raise ValueError(f'{_ValueErrorInfo}[continent, continent.name]')
        c = self.session.query(Continent) \
            .filter(Continent.name == record.name) \
            .first()
        return c


class PortDao(BaseDao[Port], ABC):

    def _get_port_by_id(self, p_id: int) -> Optional[Port]:
        """根据 ``Port.id`` 获得 :class:`Port`"""
        if p_id:
            p = self.session.query(Port).get(p_id)
            return p
        return None

    def _get_port_by_name(self, p_name: str) -> Optional[Port]:
        """根据 ``Port.name`` 获得 :class:`Port`"""
        if p_name:
            p = self.session.query(Port) \
                .filter(Port.name == p_name) \
                .first()
            return p
        return None

    def _get_port_by_class(self, p: Port) -> Optional[Port]:
        """使用 ``p.id`` 查找, 若 ``p.id`` 不可用则使用 ``p.name`` """
        if p:
            if p.id:
                return self._get_port_by_id(p.id)
            elif p.name:
                return self._get_port_by_name(p.name)
        return None

    def get_ports_by_province(self, province: Union[int, str, Province]) -> List[Port]:
        """
        根据省名 ``Province.name`` 获得该省的港口列表(:class:`Port`)

        :param province: Province.name or Province.id or Province
            若类型为Province，则使用 id 属性 查找, 若 id 不可用则使用 name 属性
        :return: 该省的港口列表，若未找到该省则返回空列表
        """
        p = ProvinceDao(self.session).get_province(province)
        if p:
            ports = self.session.query(Port) \
                .join(Port.china_port) \
                .join(ChinaPort.province) \
                .filter(Province.id == p.id) \
                .all()
            return ports
        return []

    def get_port(self, port: Union[int, str, Port]) -> Optional[Port]:
        """
        根据 ``Port.id`` or ``Port.name`` or ``Port`` 获得 :class:`Port`

        :param port: Port.id or Port.name or Port.
            若类型为Continent，则使用 id 属性 查找, 若 id 不可用则使用 name 属性查找
        :return: Port if exist or else None
        """
        if port is None:
            return None
        if type(port) == int:
            return self._get_port_by_id(port)
        elif type(port) == str:
            return self._get_port_by_name(port)
        elif type(port) == _Dao:
            return self._get_port_by_class(port)
        else:
            raise TypeError(f'{_TypeErrorInfo}[port]')

    def get_ports_by_country(self, country: Union[int, str, Country]) -> List[Port]:
        """
        根据国家名(`Country.name`)获得该国的港口列表(`Port`)

        :param country: 国家名
        :return: 该国的港口列表
        """
        c = CountryDao(self.session).get_country(country)
        if c:
            ports = self.session.query(Port) \
                .filter(Port.country_id == c.id) \
                .all()
            return ports

    def _exist(self, record: Port) -> Port:
        if Value.is_any_none_or_empty([record, record.name, record.country_id]):
            raise ValueError(f'{_ValueErrorInfo}[port, port.name, port.country_id]')
        r = self.session.query(Port) \
            .filter(Port.name == record.name) \
            .filter(Port.country_id == record.country_id) \
            .first()
        return r


class CountryDao(BaseDao[Country], ABC):

    def _get_country_by_id(self, c_id: int) -> Optional[Country]:
        """根据 ``Country.id`` 获得 :class:`Country`"""
        if c_id:
            c = self.session.query(Country).get(c_id)
            return c
        return None

    def _get_country_by_name(self, c_name: str) -> Optional[_Dao]:
        """根据 ``Country.name`` 获得 :class:`Country`"""
        if c_name:
            c = self.session.query(Country) \
                .filter(Country.name == c_name) \
                .first()
            return c
        return None

    def _get_country_by_class(self, c: Country) -> Optional[Country]:
        """使用 ``c.id`` 查找, 若 ``c.id`` 不可用则使用 ``c.name`` """
        if c:
            if c.id:
                return self._get_country_by_id(c.id)
            elif c.name:
                return self._get_country_by_name(c.name)
        return None

    def get_country(self, country: Union[int, str, Country]) -> Optional[Country]:
        """
        根据 ``Country.id`` or ``Country.name`` or ``Country`` 获得 :class:`Country`

        :param country: Country.id or Country.name or Country.
            若类型为Continent，则使用 id 属性 查找, 若 id 不可用则使用 name 属性查找
        :return: Country if exist or else None
        """
        if country is None:
            return None
        if type(country) == int:
            return self._get_country_by_id(country)
        elif type(country) == str:
            return self._get_country_by_name(country)
        elif type(country) == _Dao:
            return self._get_country_by_class(country)
        else:
            raise TypeError(f'{_TypeErrorInfo}[country]')

    def get_country_by_continent(self, continent: Union[int, str, Continent]) -> List[Country]:
        c = ContinentDao(self.session).get_continent(continent)
        if c:
            countries = self.session.query(Country) \
                .filter(Country.continent_id == c.id) \
                .all()
            return countries
        return []

    def _exist(self, record: Country) -> Country:
        if Value.is_any_none_or_empty([record, record.name]):
            raise ValueError(f'{_ValueErrorInfo}[country, country.name]')
        r = self.session.query(Country) \
            .filter(Country.name == record.name) \
            .first()
        return r


class TideDao(BaseDao[Tide], ABC):

    def get_tide_by_pid_and_date(self, pid: int, date: Union[float, datetime, struct_time],
                                 day: int = None, hour: int = None, minute: int = None,
                                 least: bool = True):
        """
        根据港口id(`Port.id`)和日期时间(`datetime`)获取该港口指定时间段内的最近一条潮汐信息

        :param least: 是否当没有数据是返回最近一条数据
        :param pid: 港口id
        :param date: 日期时间
        :param day: 最近几天，0表示当天（不考虑时分秒等）
        :param hour: 最近几小时，0表示本小时（不考虑分秒等）
        :param minute: 最近几分钟，0表示本分钟（不考虑秒等）
        :return: 该港口当时的潮汐信息

        examples:
            >>> session=db_util.get_session()
        * 查询港口号为35的2020/09/13日的最近一条数据
            >>> TideDao(session).get_tide_by_pid_and_date(35,datetime(2020,9,13,52), today=0)
        * 查询最近4小时的最近一条数据
            >>> TideDao(session).get_tide_by_pid_and_date(pid,datetime.now(), day=4)

        """
        dd = date.day - day if day is not None else date.day
        dh = date.hour - hour if hour is not None else date.hour
        dm = date.minute - minute if minute is not None else date.minute
        if day == 0:
            dh = dm = 0
        elif hour == 0:
            dm = 0
        d = datetime(date.year, date.month, dd, dh, dm)
        rel = self.session.query(Tide) \
            .filter(Tide.pid == pid)
        if least:
            tides = rel.first()
        else:
            tides = rel.filter(Tide.t >= d).first()
        return tides

    def _exist(self, record: Tide) -> Tide:
        if Value.is_any_none_or_empty([record, record.pid, record.data, record.limit, record.t]):
            raise ValueError(f'{_ValueErrorInfo}[tide, tide.pid, tide.data, tide.limit]')
        r = self.session.query(Tide) \
            .filter(Tide.pid == record.pid) \
            .filter(Tide.t == record.t) \
            .first()
        return r


class ChinaPortDao(BaseDao[ChinaPort], ABC):

    def _exist(self, record: ChinaPort) -> ChinaPort:
        if Value.is_any_none_or_empty([record, record.province_id, record.pid]):
            raise ValueError(f'{_ValueErrorInfo}[cp, cp.province_id, cp.pid')
        r = self.session.query(ChinaPort) \
            .filter(ChinaPort.pid == record.pid) \
            .first()
        return r

    def get_ports_by_province(self, province: Union[int, str, Province]) -> List[Port]:
        """
        :see:`PortDao.get_ports_by_province`
        """
        return PortDao(self.session).get_ports_by_province(province)
