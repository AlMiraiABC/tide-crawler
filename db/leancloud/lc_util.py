from datetime import date, datetime, timedelta
from typing import Callable, List, Optional

from config import LCSetting
from db.basedbutil import BaseDbUtil
from db.common import ExecState
from db.leancloud.lc_model import LCArea, LCPort, LCTide
from db.model import Area, BaseClazz, Port, Tide
from util.logger import Logger

import leancloud
from leancloud.errors import LeanCloudError
from leancloud.object_ import Object
from leancloud.query import Query


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

    def try_insert(self, obj: BaseClazz, query: Query, save: Callable[[Object, Object]], name: str):
        """
        Try to insert :param:`obj`, or update if exists.

        :param obj: Insert value.
        :param query: Try to get exists object.
        :param save: Save :param:`obj` or update exists object which get from :param:`query`
                `(queried, obj) -> None`
        :param name: obj's friendly name.
        """
        try:
            o: Object = query.first()
            save(o, obj)
            self.logger.debug(f"update {name} {o.id} successfully.")
            return ExecState.UPDATE, o
        except LeanCloudError as ex:
            if ex.code == 101:
                try:
                    save(None, obj)
                    self.logger.debug(
                        f"create new {name} {obj.id} successfully.")
                    return ExecState.CREATE, o
                except Exception as err:  # create err
                    self.logger.error(f"create {name} failed {obj.__dict__}. {err}",
                                      exc_info=True, stack_info=True)
                    return ExecState.FAIL, None
                # endregion
            self.logger.error(f"add {name} failed {obj.__dict__}. {ex}",  # others errcode
                              exc_info=True, stack_info=True)
            return ExecState.FAIL, None
        except Exception as err:  # others err
            self.logger.error(f"add {name} failed {obj.__dict__}. {err}",
                              exc_info=True, stack_info=True)
            return ExecState.FAIL, None

    def add_area(self, area: Area) -> ExecState:
        def save(o: Object, _):
            o = LCArea() if o is None else o
            o.raw = area.raw
            o.name = area.name
            o.rid = area.rid
            o.save()

        query: Query = LCArea.query
        return self.try_insert(area, query.equal_to(LCArea.NAME, area.name), save, 'area')

    def add_port(self, port: Port) -> ExecState:
        def save(o: Object, _):
            o = LCPort() if o is None else o
            o.raw = port.raw
            o.name = port.name
            o.rid = port.rid
            o.geopoint = port.geopoint if type(port.geopoint) == leancloud.GeoPoint else leancloud.GeoPoint(
                port.geopoint[0], port.geopoint[1])
            o.area = area
            o.save()

        area: LCArea = LCArea()
        # region get area
        try:
            area = LCArea.query.equal_to(
                LCArea.rid, port.area.rid).first()
        except Exception as ex:
            self.logger.error(
                f"add port area {port.area.rid} not found. {ex}", exc_info=True, stack_info=True)
            raise AttributeError(f"area {port.area_id} doesn't exist.")
        # endregion
        query: Query = LCPort.query
        return self.try_insert(port, query.equal_to(LCPort.rid, port.rid), save, 'port')

    def add_tide(self, tide: Tide) -> ExecState:
        port: LCPort = LCPort()
        t: LCTide = LCTide()
        try:
            port_query: Query = LCPort.query
            port = port_query.equal_to(LCPort.RID, tide.port_id).first()
        except Exception as ex:
            self.logger.error(
                f"add tide port {tide.port_id} not found. {ex}", exc_info=True, stack_info=True)
            raise AttributeError(f"port {tide.port_id} doesn't exist")
        try:
            t.port = port
            t.date = tide.date
            t.datum = tide.datum
            t.zone = tide.zone
            t.day = tide.day
            t.save()
            self.logger.debug(f"add tide {t.objectId} successfully.")
            return ExecState.CREATE, t
        except Exception as ex:
            self.logger.error(
                f"tide {tide} create failed. {ex}", exc_info=True, stack_info=True)
            return ExecState.FAIL, None

    def get_area(self, area_rid: str) -> Optional[Area]:
        query: Query = LCArea.query
        try:
            area: LCArea = query.equal_to(LCArea.RID, area_rid).first()
            return area
        except Exception as ex:
            self.logger.error(f"get area {area_rid} failed. {ex}",
                              exc_info=True, stack_info=True)
            return None

    def get_port(self, port_rid: str = None) -> Optional[Port]:
        query: Query = LCPort.query
        try:
            port: LCPort = query.equal_to(
                LCPort.RID, port_rid).include(LCArea).first()
            return port
        except Exception as ex:
            self.logger.error(f"get port {port_rid} failed. {ex}",
                              exc_info=True, stack_info=True)
            return None

    def get_tide(self, port_id: str, d: date) -> Optional[Tide]:
        query: Query = Tide.query
        dt = datetime(d.year, d.month, d.day)
        try:
            tide: LCTide = query.equal_to(LCTide.PORT, port_id)\
                .greater_than_or_equal_to(LCTide.DATE, dt)\
                .less_than(LCTide.DATE, dt+timedelta(1))\
                .include(LCPort.__name__)\
                .first()
            return tide
        except Exception as ex:
            self.logger.error(f"get tide {port_id}/{str(date)} failed. {ex}",
                              exc_info=True, stack_info=True)
            return None

    def get_all_areas(self) -> List[Area]:
        return LCArea.query.find()

    def get_all_ports(self) -> List[Port]:
        return LCPort.query.find()
