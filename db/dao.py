from abc import abstractmethod
from datetime import date
from typing import List, Union, Optional, Tuple, TypeVar, Generic

from sqlalchemy.orm import Session

from db.db import ExecState
from db.entity import *
from util.validate import Value

_ValueErrorInfo = 'None or Empty values: '
_TypeErrorInfo = 'Type Error: '

_Dao = TypeVar('_Dao')


class BaseDao(Generic[_Dao], ABC):
    def __init__(self, session: Session):
        self.session = session

    def insert(self, record: _Dao) -> Tuple[ExecState, _Dao]:
        """
        当数据库中未找到(根据self._exist()判断)时插入该记录

        :return: 执行结果, 数据库内的信息
        """
        r = self._exist(record)
        if r:
            return ExecState.EXIST, r
        return self._insert(record), record

    def update(self, record: _Dao) -> Tuple[ExecState, _Dao]:
        """

        :param record:
        :return:
        """
        # noinspection PyBroadException
        try:
            self.session.add(record)
            return ExecState.SUCCESS, record
        except Exception:
            return ExecState.FAIL, record

    @abstractmethod
    def _exist(self, record: _Dao) -> _Dao:
        """
        :return: record if exist or else None
        """
        pass

    def _insert(self, entity: BaseTable) -> ExecState:
        # noinspection PyBroadException
        try:
            self.session.add(entity)
            return ExecState.SUCCESS
        except Exception:
            return ExecState.FAIL


class ProvinceDao(BaseDao[Province]):

    def get_all_province(self) -> List[Province]:
        """
        获得所有省份(:class:`Province`)
        """
        provinces = self.session.query(_Dao).all()
        return provinces

    def get_province(self, province: Union[int, str, Province]) -> Optional[_Dao]:
        """
        根据 ``Province.id`` or ``Province.name`` or ``Province`` 获得 :class:`Province`

        :param province: Province.id or Province.name or Province.
            若类型为Province，则使用id属性查找, 若id不可用则使用name属性查找
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

    def _get_province_by_id(self, province_id: int) -> Optional[Province]:
        """根据 ``Province.id`` 获得 :class:`Province`"""
        if province_id:
            p = self.session.query(Province).get(province_id)
            return p
        return None

    def _get_province_by_name(self, province_name: str) -> Optional[Province]:
        """根据 ``Province.name`` 获得 :class:`Province`"""
        if province_name:
            p = self.session.query(Province).filter(Province.name == province_name).first()
            return p
        return None

    def _get_province_by_class(self, province: Province) -> Optional[Province]:
        """使用 ``province.id`` 查找, 若 ``province.id`` 不可用则使用 ``p.name`` """
        if province:
            if province.id:
                return self._get_province_by_id(province.id)
            elif province.name:
                return self._get_province_by_name(province.name)
        return None

    def _exist(self, province: Province) -> Province:
        """
        数据库中是否存在(:prop:`province.name`)
        """
        if Value.is_any_none_or_empty([province, province.name]):
            raise ValueError(_ValueErrorInfo)
        r = self.session.query(Province) \
            .filter(Province.name == province.name) \
            .first()
        return r


class CityDao(BaseDao[City]):

    def __init__(self, session: Session):
        super().__init__(session)
        self.stmt = self.session.query(City) \
            .join(Province, City.province_id == Province.id)

    def get_cities(self, province: Union[int, str, Province]) -> List[City]:
        if type(province) == int:
            return self._get_cities_by_id(province)
        if type(province) == str:
            return self._get_cities_by_name(province)
        if type(province) == Province:
            return self._get_cities_by_class(province)
        raise TypeError(f'{_TypeErrorInfo}[province]')

    def _get_cities_by_id(self, province_id: int) -> List[City]:
        """get all cities by province.id """
        if province_id:
            cities = self.stmt \
                .filter(Province.id == province_id) \
                .all()
            return cities
        return []

    def _get_cities_by_name(self, province_name: str) -> List[City]:
        """get all cities by province.name"""
        if province_name:
            cities = self.stmt.filter(Province.name == province_name).all
            return cities
        return []

    def _get_cities_by_class(self, province: Province) -> List[City]:
        if province:
            if province.id:
                return self._get_cities_by_id(province.id)
            if province.name:
                return self._get_cities_by_name(province.name)
        return []

    def _exist(self, city: City) -> City:
        """
        数据库中是否存在(:prop:`city.name`)
        """
        if Value.is_any_none_or_empty([city, city.name]):
            raise ValueError(_ValueErrorInfo)
        r = self.session.query(City) \
            .filter(City.name == city.name) \
            .first()
        return r


class TideDao(BaseDao[Tide], ABC):

    def get_tide_by_district_and_date(self, district_id: int, day: date) -> Optional[Tide]:
        """
        根据地区id(:param:`district_id`)和日期(:param:`day`)获取该港口指定时间段内的最近一条潮汐信息

        :param district_id: id of district
        :param day: date
        :return: record if find or else None
        """
        tide = self.session.query(Tide) \
            .filter(Tide.district_id == district_id, Tide.day == day) \
            .first()
        return tide

    def _exist(self, record: Tide) -> Tide:
        if Value.is_any_none_or_empty([record, record.district_id, record.day]):
            raise ValueError(_ValueErrorInfo)
        r = self.session.query(Tide) \
            .filter(Tide.district_id == record.district_id, Tide.day==record.day) \
            .first()
        return r
