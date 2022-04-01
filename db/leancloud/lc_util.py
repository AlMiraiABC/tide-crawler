from datetime import date, datetime, timedelta
from typing import Any, Callable, List, Optional, Tuple, Type, Union, overload

from config import LCSetting
from db.basedbutil import IDT, BaseDbUtil, switch_idt
from db.common import ExecState
from db.leancloud.lc_model import (LCArea, LCBaseClazz, LCPort, LCProvince,
                                   LCTide, LCWithInfo)
from db.model import Area, BaseClazz, Port, Province, Tide, WithInfo
from util.logger import Logger
from util.validate import Value

import leancloud
from leancloud import LeanCloudError, Query


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
        self.open()
        # alias
        self.login = self.open
        self.logout = self.close

    def open(self) -> None:
        """
        Login with a special User which has auths to create, delete, find, get, update

        It will do nothing if have logged in. Use :method:`close` to logout before re-login.

        See also
        ------
        https://leancloud.cn/docs/leanstorage_guide-python.html#hash964666
        """
        if leancloud.User.get_current() is not None:
            return
        leancloud.User().login(LCSetting.USERNAME,
                               LCSetting.PASSWORD)

    def close(self) -> None:
        """
        Logout current user. Use :method:`open` to re-login.

        See also
        ------
        https://leancloud.cn/docs/leanstorage_guide-python.html#hash748191977
        """
        user = leancloud.User.get_current()
        user and user.logout()

    def __save(self, obj: LCBaseClazz):
        try:
            obj.save()
            self.logger.debug(
                f"create new {type(obj).__name__} {obj.id} successfully.")
            return ExecState.CREATE, obj
        except Exception as err:  # create err
            self.logger.error(f"create {type(obj).__name__} failed {obj.__dict__}. {err}",
                              exc_info=True, stack_info=True)
            return ExecState.FAIL, None

    def __get(self, obj: LCWithInfo, col: IDT, clazz: Type[LCBaseClazz], rid_query: Callable[[], LCBaseClazz] = None):
        return self.__get_by_id(switch_idt(col, obj.id, obj.rid), col, clazz, rid_query)

    def __get_by_id(self, id: str, col: IDT, clazz: Type[LCBaseClazz], rid_query: Callable[[], LCBaseClazz] = None) -> Tuple[ExecState, Optional[LCBaseClazz]]:
        q: Query = clazz.query
        rid_query = rid_query if callable(
            rid_query) else lambda: q.equal_to(clazz.RID, id).first()
        try:
            # TODO consider using `clazz.create_without_data`` instead of `q.get``
            return switch_idt(col, lambda: (ExecState.EXIST, q.get(id)), lambda: (ExecState.EXIST, rid_query()))
        except Exception as ex:
            errmsg = f'occured an error when get object by {col}({id}). {ex}'
            return self.__lcex_wrapper(ex, errmsg, lambda: (ExecState.UN_EXIST, None), lambda: (ExecState.FAIL, None))

    def __lcex_wrapper(self, ex: Exception, errmsg: str, unexist_cb: Callable[[], Any], err_cb: Callable[[], Any]):
        """
        LeanCloud exception wrapper.

        :param ex: Occured exception.
        :param errmsg: Logged message if :param:`ex` is :class:`LeanCloudError` and it's code==101.
        :param unexist_cb: Callback if :param:`ex` is :class:`LeanCloudError` and it's code==101.
        :param err_cb: Callbackk if others.
        """
        if isinstance(ex, LeanCloudError) and ex.code == 101:
            return unexist_cb()
        self.logger.error(errmsg, exc_info=True, stack_info=True)
        return err_cb()

    def __before_save(self, obj: Optional[BaseClazz], find: Optional[LCBaseClazz], clazz: Type[LCBaseClazz]) -> LCBaseClazz:
        if find is None:
            if isinstance(obj, LCBaseClazz):
                return obj
            return clazz()
        return find

    def try_insert(self, obj: WithInfo, col: IDT, save: Callable[[Optional[LCWithInfo]], LCWithInfo], clazz: Type[LCWithInfo], rid_query: Callable[[], LCBaseClazz] = None) -> Tuple[ExecState, Optional[WithInfo]]:
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
        r, o = self.__get(obj, col, clazz, rid_query)
        ins = save(o)
        try:
            if r == ExecState.UN_EXIST:
                raise LeanCloudError(101,'')
            if r == ExecState.FAIL:
                return ExecState.FAIL, None
            if r == ExecState.EXIST:
                self.logger.debug(
                    f"update {type(ins).__name__} {ins.id} successfully.")
                ins.save()
                return ExecState.UPDATE, ins
        except Exception as ex:
            errmsg = f"add {type(ins).__name__} failed {ins.__dict__}. {ex}"
            return self.__lcex_wrapper(ex, errmsg, lambda: self.__save(save(None)), lambda: (ExecState.FAIL, None))

    def add_area(self, area: Area, col: IDT) -> Tuple[ExecState, BaseClazz]:
        def save(o: Optional[LCArea]):
            o = self.__before_save(area, o, LCArea)
            o.raw = area.raw
            o.name = area.name
            o.rid = area.rid
            return o

        return self.try_insert(area, col, save, LCArea)

    def add_province(self, province: Province, col: IDT) -> Tuple[ExecState, Optional[BaseClazz]]:
        def save(o: LCProvince):
            o = self.__before_save(province, o, LCProvince)
            o.raw = province.raw
            o.area = area
            o.name = province.name
            o.rid = province.rid

        (ret, area) = self.__get(province.area, col, LCArea)
        if ret != ExecState.EXIST:
            raise ValueError(f'the area {province.area} is not exist.')
        q: Query = LCProvince.query
        return self.try_insert(province, col, save, LCProvince, q.equal_to(LCProvince.RID, province.rid).equal_to(LCProvince.AREA, area))

    def add_port(self, port: Port, col: IDT) -> Tuple[ExecState, BaseClazz]:
        def save(o: Optional[LCPort]):
            o = self.__before_save(port, o, LCPort)
            o.raw = port.raw
            o.name = port.name
            o.rid = port.rid
            o.geopoint = port.geopoint if type(port.geopoint) == leancloud.GeoPoint else leancloud.GeoPoint(
                port.geopoint[0], port.geopoint[1])
            o.province = province
            o.zone = port.zone
            return o

        (ret, province) = self.__get(port.province, col, LCProvince)
        if ret != ExecState.EXIST:
            raise ValueError(f'the province {port.province} is not exist.')
        query: Query = LCPort.query
        return self.try_insert(port, col, save, LCPort, query.equal_to(LCPort.RID, port.rid).equal_to(LCPort.PROVINCE, province))

    def add_tide(self, tide: Tide, col: IDT) -> Tuple[ExecState, BaseClazz]:
        port: LCPort = LCPort()
        t: LCTide = LCTide()
        (ret, port) = self.__get(tide.port, col, LCPort)
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
        return ExecState.FAIL, None

    def get_area(self, area_id: str, col: IDT) -> Optional[Area]:
        try:
            return self.__get_by_id(area_id, col, LCArea)
        except Exception as ex:
            self.logger.error(f"get area {area_id} failed. {ex}",
                              exc_info=True, stack_info=True)
        return None

    def get_province(self, province_id: str, col: IDT) -> Optional[Province]:
        try:
            return self.__get_by_id(province_id, col, LCProvince)
        except Exception as ex:
            self.logger.error(f"get province {province_id} failed. {ex}",
                              exc_info=True, stack_info=True)
        return None

    def get_port(self, port_rid: str = None) -> Optional[Port]:
        query: Query = LCPort.query
        try:
            port: LCPort = query.equal_to(
                LCPort.RID, port_rid).include(LCPort).first()
            return port
        except Exception as ex:
            self.logger.error(f"get port {port_rid} failed. {ex}",
                              exc_info=True, stack_info=True)
        return None

    def get_tide(self, port_id: str, d: date) -> Optional[Tide]:
        query: Query = LCTide.query
        dt = datetime(d.year, d.month, d.day)
        try:
            return query.equal_to(LCTide.PORT, port_id) \
                .greater_than_or_equal_to(LCTide.DATE, dt) \
                .less_than(LCTide.DATE, dt+timedelta(1)) \
                .include(LCPort.__name__) \
                .first()
        except Exception as ex:
            self.logger.error(f"get tide {port_id}({str(date)}) failed. {ex}",
                              exc_info=True, stack_info=True)
        return None

    def get_areas(self) -> List[Area]:
        try:
            return LCArea.query.find()
        except Exception as ex:
            self.logger.error(f"get areas failed. {ex}",
                              exc_info=True, stack_info=True)
        return []

    @overload
    def get_provinces(self, area: Area) -> List[Province]:
        pass

    @overload
    def get_provinces(self, area: str, col: IDT) -> List[Province]:
        pass

    def __get_provinces_area_str(self, area: str, col: IDT) -> List[Province]:
        if Value.is_any_none_or_whitespace(area):
            raise ValueError('area cannot be none or empty.')
        q: Query = LCProvince.query
        try:
            a = self.__get_by_id(area, col, LCArea)
            if a is None:
                raise ValueError(f'area({area}) not found')
            return q.equal_to(LCProvince.AREA, area).find()
        except Exception as ex:
            self.logger.error(f'get provinces by {area} failed. {ex}')
        return []

    def __get_provinces_area_clazz(self, area: Area) -> List[Province]:
        if area is None or Value.is_any_none_or_whitespace(area.objectId):
            raise ValueError('area or area.objectId cannot be none or empty.')
        q: Query = LCProvince.query
        try:
            return q.equal_to(LCProvince.AREA, area).find()
        except Exception as ex:
            self.logger.error(f"get provinces by {area.objectId} failed. {ex}",
                              exc_info=True, stack_info=True)
        return []

    def get_provinces(self, area: Union[Area, str], col: IDT = 'id') -> List[Province]:
        if isinstance(area, str):
            return self.__get_provinces_area_str(area, col)
        elif isinstance(area, LCArea):
            return self.__get_provinces_area_clazz(area)
        raise TypeError(
            f'type of area must be {str.__name__} or {LCArea.__name__}, but got {type(area)}')

    @overload
    def get_ports(self, province: Province) -> List[Port]:
        pass

    @overload
    def get_ports(self, province: str, col: IDT) -> List[Port]:
        pass

    def __get_ports_province_str(self, province: str, col: IDT) -> List[Port]:
        if Value.is_any_none_or_whitespace(province):
            raise ValueError('province cannot be none or empty.')
        q: Query = LCProvince.query
        try:
            p = self.__get_by_id(province, col, LCProvince)
            if p is None:
                raise ValueError(f'province({province}) not found')
            return q.equal_to(LCProvince.AREA, province).find()
        except Exception as ex:
            self.logger.error(f'get ports by {province} failed. {ex}')
        return []

    def __get_ports_province_clazz(self, province: Province) -> List[Port]:
        if province is None or Value.is_any_none_or_whitespace(province.objectId):
            raise ValueError('area or area.objectId cannot be none or empty.')
        q: Query = LCPort.query
        try:
            return q.equal_to(LCPort.PROVINCE, province).find()
        except Exception as ex:
            self.logger.error(f"get ports by {province.objectId} failed. {ex}",
                              exc_info=True, stack_info=True)
        return []

    def get_ports(self, province: Union[Province, str], col: IDT) -> List[Port]:
        if isinstance(province, str):
            return self.__get_ports_province_str(province, col)
        elif isinstance(province, LCArea):
            return self.__get_ports_province_clazz(province)
        raise TypeError(
            f'type of province must be {str.__name__} or {LCProvince.__name__}, but got {type(province)}')
