import asyncio
import functools
from datetime import date, datetime, timedelta
from typing import (Any, Callable, List, Optional, Tuple, Type, TypeVar, Union,
                    overload)

from config import LCSetting
from db.basedbutil import IDT, BaseDbUtil, switch_idt
from db.common import ExecState
from db.leancloud.lc_model import (LCArea, LCPort, LCProvince, LCTide,
                                   LCWithInfo)
from db.model import Area, Port, Province, Tide, WithInfo
from util.async_util import async_wrap
from util.logger import Logger
from util.validate import Value

import leancloud
from leancloud import LeanCloudError, Query

_Clazz = TypeVar('_Clazz', bound=LCWithInfo)
_ObjClazz = TypeVar('_ObjClazz', bound=WithInfo)


def _login():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            if leancloud.User.get_current() is None:
                leancloud.User().login(LCSetting.USERNAME, LCSetting.PASSWORD)
            return await func(*args, **kwargs)
        return wrapped
    return wrapper


class LCUtil(BaseDbUtil):
    """
    util for LeanCloud

    See also
    ------
    https://leancloud.cn/docs/leanstorage_guide-python.html
    """

    def __init__(self) -> None:
        """
        create connection to leancloud data storage and login with config

        Please use :class:`LeanCloudSetting` to set params

        See also
        ------
        https://leancloud.cn/docs/sdk_setup-python.html#hash20935048
        """
        self.logger = Logger(self.__class__.__name__).logger
        id = LCSetting.APP_ID
        key = LCSetting.APP_KEY if LCSetting.APP_KEY else LCSetting.MASTER_KEY
        leancloud.init(id, key)
        asyncio.ensure_future(self.open())
        # alias
        self.login = self.open
        self.logout = self.close

    @_login()
    async def open(self) -> None:
        """
        Login with a special User which has auths to create, delete, find, get, update

        It will do nothing if have logged in. Use :method:`close` to logout before re-login.

        See also
        ------
        https://leancloud.cn/docs/leanstorage_guide-python.html#hash964666
        """
        pass

    async def close(self) -> None:
        """
        Logout current user. Use :method:`open` to re-login.

        See also
        ------
        https://leancloud.cn/docs/leanstorage_guide-python.html#hash748191977
        """
        user = leancloud.User.get_current()
        user and await async_wrap(user.logout)()

    def __save(self, obj: _Clazz) -> Tuple[ExecState, Union[_Clazz, Exception]]:
        """
        Save this leancloud object :param:`obj`

        :param obj: Leancloud object instance.
        :returns: 1. execute state
                  2. saved instance or exception if failed.
        """
        try:
            obj.save()
            self.logger.debug(
                f"create new {type(obj).__name__} {obj.id} successfully.")
            return ExecState.CREATE, obj
        except Exception as err:  # create err
            self.logger.error(f"create {type(obj).__name__} failed {obj.__dict__}. {err}",
                              exc_info=True, stack_info=True)
            return ExecState.FAIL, err

    @_login()
    async def __get(self, obj: _ObjClazz, col: IDT, clazz: Type[_Clazz], rid_query: Callable[[], _Clazz] = None):
        """Wrapper for :fun:`__get_by_id` to get `objid` from :param:`obj`"""
        return await self.__get_by_id(switch_idt(col, obj.id, obj.rid), col, clazz, rid_query)

    @_login()
    async def __get_by_id(self, objid: str, col: IDT, clazz: Type[_Clazz], rid_query: Callable[[], _Clazz] = None) -> Tuple[ExecState, Union[Optional[_Clazz], Exception]]:
        """
        Get a saved leancloud object instance.

        :param objid: Object id or rid to get.
        :param col: Compared column. Determine :param:`objid` is `id` or `rid`
        :param clazz: Type of this leancloud object.
        :param rid_query: :class:`Query` to get a leancloud object instance if `col==IDT.RID`
        :returns:   First item: execute result.
                    Second item: Found object, or None if doesn't exist, or Exception if occured an error.
        """
        q: Query = clazz.query
        rid_query = rid_query if callable(
            rid_query) else lambda: q.equal_to(clazz.RID, objid).first()

        def id_cb():
            return (ExecState.UN_EXIST, None) \
                if Value.is_any_none_or_whitespace(objid) \
                else (ExecState.EXIST, q.get(objid))
        try:
            # TODO consider using `clazz.create_without_data`` instead of `q.get``
            return switch_idt(col, id_cb, lambda: (ExecState.EXIST, rid_query()))
        except Exception as ex:
            errmsg = f'occured an error when get object by {col}({objid}). {ex}'
            return self.__lcex_wrapper(ex, errmsg, lambda: (ExecState.UN_EXIST, None), lambda: (ExecState.FAIL, ex))

    def __lcex_wrapper(self, ex: Exception, errmsg: str, unexist_cb: Callable[[], Any], err_cb: Callable[[], Any]):
        """
        LeanCloud exception wrapper.

        :param ex: Occured exception.
        :param errmsg: Logged message if :param:`ex` is :class:`LeanCloudError` and it's code==101.
        :param unexist_cb: Callback if :param:`ex` is :class:`LeanCloudError` and it's code==101.
        :param err_cb: Callback if others.
        """
        if isinstance(ex, LeanCloudError) and ex.code == 101:
            return unexist_cb()
        self.logger.error(errmsg, exc_info=True, stack_info=True)
        return err_cb()

    def __before_save(self, obj: Optional[_ObjClazz], find: Optional[_Clazz], clazz: Type[_Clazz]) -> _Clazz:
        if find is None:
            if isinstance(obj, clazz):
                return obj
            return clazz()
        return find

    @_login()
    async def try_insert(self, obj: _ObjClazz, col: IDT, save: Callable[[Optional[_Clazz]], _Clazz], clazz: Type[_Clazz], rid_query: Callable[[], _Clazz] = None) -> Tuple[ExecState, Union[_Clazz, Exception]]:
        """
        Try to insert :param:`obj`, or update if exists.

        :param obj: Object which will be inserted.
        :param col: Compared column.
        :param save: Get an instance to save or update.
            Args:
                - Queried object from :param:`query`
            Returns:
                An object to create or insert.
        :param clazz: Inserted object class type.
        :param rid_query: Query callback if `col=='rid'.
        :return: (execute-state, inserted-or-updated-object)
        """
        r, o = await self.__get(obj, col, clazz, rid_query)
        try:
            if r == ExecState.FAIL:
                return ExecState.FAIL, o
            ins = save(o)
            if not isinstance(ins, LCWithInfo):
                raise TypeError(
                    f"Except {LCWithInfo.__name__} but got {type(ins)} from :param:`save`")
            if r == ExecState.UN_EXIST:
                raise LeanCloudError(101, '')  # to save
            if r == ExecState.EXIST:
                await async_wrap(ins.save)()
                self.logger.debug(
                    f"update {type(ins).__name__} {ins.id} successfully.")
                return ExecState.UPDATE, ins
        except Exception as ex:
            errmsg = f"add {type(ins).__name__} failed {ins.__dict__}. {ex}"
            return self.__lcex_wrapper(ex, errmsg, lambda: self.__save(save(None)), lambda: (ExecState.FAIL, ex))

    @_login()
    async def add_area(self, area: Area, col: IDT) -> Tuple[ExecState, Union[LCArea, Exception]]:
        def save(o: Optional[LCArea]):
            o = self.__before_save(area, o, LCArea)
            o.raw = area.raw
            o.name = area.name
            o.rid = area.rid
            return o

        return await self.try_insert(area, col, save, LCArea)

    @_login()
    async def add_province(self, province: Province, col: IDT) -> Tuple[ExecState, Union[LCProvince, Exception]]:
        def save(o: LCProvince):
            o = self.__before_save(province, o, LCProvince)
            o.raw = province.raw
            o.area = area
            o.name = province.name
            o.rid = province.rid
            return o

        (ret, area) = await self.__get(province.area, col, LCArea)
        if ret != ExecState.EXIST:
            raise ValueError(f'the area {province.area} is not exist.')
        q: Query = LCProvince.query
        return await self.try_insert(province, col, save, LCProvince, q.equal_to(LCProvince.RID, province.rid).equal_to(LCProvince.AREA, area))

    @_login()
    async def add_port(self, port: Port, col: IDT) -> Tuple[ExecState, Union[LCPort, Exception]]:
        def save(o: Optional[LCPort]):
            o = self.__before_save(port, o, LCPort)
            o.raw = port.raw
            o.name = port.name
            o.rid = port.rid
            o.geopoint = port.geopoint
            o.province = province
            o.zone = port.zone
            return o

        (ret, province) = await self.__get(port.province, col, LCProvince)
        if ret != ExecState.EXIST:
            raise ValueError(f'the province {port.province} is not exist.')
        query: Query = LCPort.query
        return await self.try_insert(port, col, save, LCPort, query.equal_to(LCPort.RID, port.rid).equal_to(LCPort.PROVINCE, province))

    @_login()
    async def add_tide(self, tide: Tide, col: IDT) -> Tuple[ExecState, Union[LCTide, Exception]]:
        def save(o: Optional[LCTide]):
            o = self.__before_save(tide, o, LCTide)
            o.port = tide.port
            o.date = tide.date
            o.datum = tide.datum
            o.day = tide.day
            o.limit = tide.limit

    async def add_tide(self, tide: Tide, col: IDT) -> Tuple[ExecState, Union[Optional[LCTide], Exception]]:
        t: LCTide = LCTide()
        (ret, port) = await self.__get(tide.port, col, LCPort)
        if ret != ExecState.EXIST:
            raise ValueError(f'the port {tide.port} is not exist.')
        try:
            t.port = port
            t.date = tide.date
            t.datum = tide.datum
            t.day = tide.day
            t.limit = tide.limit
            t.save()
            self.logger.debug(f"add tide {t.objectId} successfully.")
            return ExecState.CREATE, t
        except Exception as ex:
            self.logger.error(
                f"tide {tide} create failed. {ex}", exc_info=True, stack_info=True)
            return ExecState.FAIL, ex

    @_login()
    async def get_area(self, area_id: str, col: IDT) -> Optional[LCArea]:
        try:
            return await self.__get_by_id(area_id, col, LCArea)[1]
        except Exception as ex:
            self.logger.error(f"get area {area_id} failed. {ex}",
                              exc_info=True, stack_info=True)
        return None

    @_login()
    async def get_province(self, province_id: str, col: IDT) -> Optional[LCProvince]:
        try:
            return await self.__get_by_id(province_id, col, LCProvince)[1]
        except Exception as ex:
            self.logger.error(f"get province {province_id} failed. {ex}",
                              exc_info=True, stack_info=True)
        return None

    @_login()
    async def get_port(self, port_id: str, col: IDT) -> Optional[LCPort]:
        try:
            return await self.__get_by_id(port_id, col, LCPort)[1]
        except Exception as ex:
            self.logger.error(f"get port {port_id} failed. {ex}",
                              exc_info=True, stack_info=True)
        return None

    @_login()
    async def get_tide(self, port_id: str, d: date) -> Optional[LCTide]:
        query: Query = LCTide.query
        dt = datetime(d.year, d.month, d.day)
        try:
            return await async_wrap(query.equal_to(LCTide.PORT, LCTide.create_without_data(port_id))
                                    .greater_than_or_equal_to(LCTide.DATE, dt)
                                    .less_than(LCTide.DATE, dt+timedelta(1))
                                    .include(LCPort.__name__)
                                    .first)()
        except Exception as ex:
            self.logger.error(f"get tide {port_id}({str(date)}) failed. {ex}",
                              exc_info=True, stack_info=True)
        return None

    @_login()
    async def get_areas(self) -> List[LCArea]:
        try:
            return await async_wrap(LCArea.query.find)()
        except Exception as ex:
            self.logger.error(f"get areas failed. {ex}",
                              exc_info=True, stack_info=True)
        return []

    @overload
    @_login()
    async def get_provinces(self, area: Area) -> List[LCProvince]:
        pass

    @overload
    @_login()
    async def get_provinces(self, area: str, col: IDT) -> List[LCProvince]:
        pass

    @_login()
    async def __get_provinces_area_str(self, area: str, col: IDT) -> List[LCProvince]:
        if Value.is_any_none_or_whitespace(area):
            raise ValueError('area cannot be none or empty.')
        q: Query = LCProvince.query
        try:
            (_, a) = await self.__get_by_id(area, col, LCArea)
            if a is None:
                raise ValueError(f'area({area}) not found')
            return await async_wrap(q.equal_to(LCProvince.AREA, a).find)()
        except Exception as ex:
            self.logger.error(f'get provinces by {area} failed. {ex}')
        return []

    @_login()
    async def __get_provinces_area_clazz(self, area: Area) -> List[LCProvince]:
        if area is None or Value.is_any_none_or_whitespace(area.objectId):
            raise ValueError('area or area.objectId cannot be none or empty.')
        q: Query = LCProvince.query
        try:
            return await async_wrap(q.equal_to(LCProvince.AREA, LCArea.create_without_data(Area.objectId))
                                    .find)()
        except Exception as ex:
            self.logger.error(f"get provinces by {area.objectId} failed. {ex}",
                              exc_info=True, stack_info=True)
        return []

    @_login()
    async def get_provinces(self, area: Union[Area, str], col: IDT = None) -> List[LCProvince]:
        if isinstance(area, str):
            return await self.__get_provinces_area_str(area, col)
        elif isinstance(area, LCArea):
            return await self.__get_provinces_area_clazz(area)
        raise TypeError(
            f'type of area must be {str.__name__} or {LCArea.__name__}, but got {type(area)}')

    @overload
    @_login()
    async def get_ports(self, province: Province) -> List[LCPort]:
        pass

    @overload
    @_login()
    async def get_ports(self, province: str, col: IDT) -> List[LCPort]:
        pass

    @_login()
    async def __get_ports_province_str(self, province: str, col: IDT) -> List[LCPort]:
        if Value.is_any_none_or_whitespace(province):
            raise ValueError('province cannot be none or empty.')
        q: Query = LCPort.query
        try:
            (_, p) = await self.__get_by_id(province, col, LCProvince)
            if p is None:
                raise ValueError(f'province({province}) not found')
            return await async_wrap(q.equal_to(LCPort.PROVINCE, p).find)()
        except Exception as ex:
            self.logger.error(f'get ports by {province} failed. {ex}')
        return []

    @_login()
    async def __get_ports_province_clazz(self, province: Province) -> List[LCPort]:
        if province is None or Value.is_any_none_or_whitespace(province.objectId):
            raise ValueError(
                'province and province.objectId cannot be none or empty.')
        q: Query = LCPort.query
        try:
            return await async_wrap(q.equal_to(LCPort.PROVINCE, province).find)()
        except Exception as ex:
            self.logger.error(f"get ports by {province.objectId} failed. {ex}",
                              exc_info=True, stack_info=True)
        return []

    @_login()
    async def get_ports(self, province: Union[Province, str], col: IDT = None) -> List[LCPort]:
        if isinstance(province, str):
            return await self.__get_ports_province_str(province, col)
        elif isinstance(province, LCProvince):
            return await self.__get_ports_province_clazz(province)
        raise TypeError(
            f'type of province must be {str.__name__} or {LCProvince.__name__}, but got {type(province)}')
