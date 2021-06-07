from typing import List, Union, Tuple, TypeVar, Generic, Optional

from db.dao import ContinentDao, CountryDao, ProvinceDao, PortDao, ChinaPortDao
from db.entity import *
from db.db import db_util, ExecState

_Dao = TypeVar('_Dao')
_Table = TypeVar('_Table')


class BaseService(Generic[_Dao, _Table]):

    @classmethod
    def insert_one(cls, record: _Table) -> Tuple[ExecState, _Table]:
        session = db_util.get_session()
        s, r = _Dao(session).insert(record)
        db_util.close_session(session)
        return s, r

    @classmethod
    def insert_many(cls, records: List[_Table]) -> Tuple[List[_Table], List[_Table], List[_Table]]:
        """
        插入多条记录

        :return: (ExecState.SUCCESS, ExecState.EXIST, ExecState.FAIL)
        """
        successes: List[_Table] = []
        fails: List[_Table] = []
        exists: List[_Table] = []
        for record in records:
            s, r = cls.insert_one(record)
            if s == ExecState.SUCCESS:
                successes.append(r)
            elif s == ExecState.EXIST:
                exists.append(r)
            else:
                fails.append(r)
        return successes, exists, fails


class ContinentService(BaseService[ContinentDao, Continent]):
    @classmethod
    def get_all_continent(cls) -> List[Continent]:
        """
        获取所有大洲(:class:`Continent`)信息

        :return: List[Continent]
        """
        session = db_util.get_session()
        ret = ContinentDao(session).get_all_continent()
        db_util.close_session(session)
        return ret


class CountryService(BaseService[CountryDao, Country]):
    china: Country = None

    @classmethod
    def get_all_country_by_continent(cls, continent: Union[int, str, Continent]) -> List[Country]:
        session = db_util.get_session()
        ret = CountryDao(session).get_country_by_continent(continent)
        db_util.close_session(session)
        return ret

    @classmethod
    def get_china(cls, update: bool = False) -> Optional[Country]:
        if not CountryService.china or update:
            session = db_util.get_session()
            CountryService.china = CountryDao(session).get_country('中国')
            db_util.close_session(session)
        return CountryService.china


class ProvinceService(BaseService[ProvinceDao, Province]):
    @classmethod
    def get_all_province(cls) -> List[Province]:
        session = db_util.get_session()
        ret = ProvinceDao(session).get_all_province()
        db_util.close_session(session)
        return ret


class PortService(BaseService[PortDao, Port]):
    @classmethod
    def get_all_port_by_country(cls, country: Country) -> List[Port]:
        session = db_util.get_session()
        ret = PortDao(session).get_ports_by_country(country)
        db_util.close_session(session)
        return ret

    @classmethod
    def get_all_port_by_province(cls, province: Province) -> List[Port]:
        session = db_util.get_session()
        ret = PortDao(session).get_ports_by_province(province)
        db_util.close_session(session)
        return ret

    @classmethod
    def insert_one(cls, record: _Table, province: Union[int, str, Province] = None) -> Tuple[ExecState, _Table]:
        """
        插入一条港口记录
        当是中国(record.country_id是中国的id)的港口时， ``province`` 不得为空；
        若 ``province`` 不在数据库，则插入该 ``province`` ，
        同时，在 ``china_port`` 中插入一条港口和省份的关联。

        :raise: 当是中国的港口时，``province`` 为空则抛出 :class:`ValueError`
        :return: 是否插入成功, 数据库中的port记录
        """

        def session_error():
            session.rollback()
            session.close()

        session = db_util.get_session()
        port_state, port_record = PortDao(session).insert(record)
        if port_state == ExecState.FAIL:
            return ExecState.EXIST, port_record
        # 如果port.country_id是中国
        if record.country_id == CountryService.get_china().id:
            if not province:
                session_error()
                raise ValueError('如果国家为中国，则province不得为空')
            prov_state, prov_record = ProvinceDao(session).insert(province)
            if prov_state == ExecState.FAIL:
                session_error()
                return ExecState.FAIL, record
            cp_state, cp_record = ChinaPortDao(session).insert(
                ChinaPort(pid=port_record.id, province_id=prov_record.id))
            if cp_state == ExecState.FAIL:
                session_error()
                return ExecState.FAIL, record
            db_util.close_session(session)
        return port_state, port_record
