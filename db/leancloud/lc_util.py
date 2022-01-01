from datetime import date
from typing import List, Optional

from config import LCSetting
from crawler.model.location import AreaInfo, PortInfo
from crawler.model.tide import Tide, TideDay, TideLimit
from db.common import ExecState
from db.basedbutil import BaseDbUtil
from db.leancloud.model import Area, Port
from db.leancloud.model import Tide as LCTide
from db.leancloud.model import TideItem
from util.logger import Logger

import leancloud
from leancloud.errors import LeanCloudError
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

    def add_area(self, area: AreaInfo) -> ExecState:

        def save():
            exist.raw = area.raw
            exist.name = area.name
            exist.rid = area.id
            exist.save()

        query: Query = Area.query
        exist: Area = None
        try:
            if not area.name or area.name.isspace():
                raise AttributeError("area name cannot be null or empty")
            exist = query.equal_to(Area.NAME, area.name).first()
            save()  # update
            return ExecState.UPDATE
        except LeanCloudError as ex:
            if ex.code == 101:  # not exist
                exist = area
                try:
                    save()  # create
                    return ExecState.CREATE
                except Exception as e:  # create err
                    self.logger.error(f"create area {area.name} failed. {e}",
                                      exc_info=True, stack_info=True)
                    return ExecState.FAIL
            self.logger.error(f"update area {area.name} failed. {ex}",  # others errcode
                              exc_info=True, stack_info=True)
            return ExecState.FAIL
        except Exception as e:  # others err
            self.logger.error(f"update area {area.name} failed. {e}",
                              exc_info=True, stack_info=True)
            return ExecState.FAIL

    def add_port(self, port: PortInfo) -> ExecState:
        def save():
            exist.raw = port.raw
            exist.name = port.name
            exist.rid = port.id
            exist.save()

        query: Query = Port.query
        exist: Port = None
        try:
            exist = query.equal_to(Port.NAME, port.name).first()
            save()  # update
            return ExecState.UPDATE
        except LeanCloudError as ex:
            if ex.code == 101:  # not exist
                exist = PortInfo()
                try:
                    save()  # create
                    return ExecState.CREATE
                except Exception as e:  # create err
                    self.logger.error(f"create port {port.name} failed. {e}",
                                      exc_info=True, stack_info=True)
                    return ExecState.FAIL
            self.logger.error(f"update port {port.name} failed. {ex}",  # others errcode
                              exc_info=True, stack_info=True)
            return ExecState.FAIL
        except Exception as e:  # others err
            self.logger.error(f"update area {port.name} failed. {e}",
                              exc_info=True, stack_info=True)
            return ExecState.FAIL

    def add_tide(self, day: TideDay, limit: TideLimit, port_id: str, zone: str = "+8:00", datum: float = 0, date: date = ...) -> ExecState:
        dc = [TideItem(d.time, d.height) for d in day]
        lc = [TideItem(l.time, l.height) for l in limit]
        tc = Tide()
        tc.day = dc
        tc.limit = lc
        tc.date = date
        tc.datum = datum
        tc.zone = zone
        port_query: Query = Port.query
        port: Port = None
        try:
            port = port_query.equal_to(Port.RID, port_id).first()
            tc.port = port
        except LeanCloudError as ex:
            self.logger.error(
                f"port {port_id} not exist {ex}", exc_info=True, stack_info=True)
            return ExecState.FAIL
        try:
            tc.save()
            return ExecState.CREATE
        except Exception as ex:
            self.logger.error(
                f"tide {port_id}/{date.isoformat()} create failed")

    def get_area(self, area_id: str) -> Optional[AreaInfo]:
        query: Query = Area.query
        try:
            area: Area = query.equal_to(Area.RID, area_id).first()
            return AreaInfo(area.rid, area.name, area.raw)
        except Exception as ex:
            self.logger.error(f"get area {area_id} failed. {ex}",
                              exc_info=True, stack_info=True)
            return None

    def get_port(self, port_id: str = None) -> Optional[PortInfo]:
        query: Query = Port.query
        try:
            port: Port = query.equal_to(
                Port.RID, port_id).include(Area.__name__).first()
            return PortInfo(port.area.rid, port.rid, port.latitude, port.longitude, port.name, port.raw)
        except Exception as ex:
            self.logger.error(f"get port {port_id} failed. {ex}",
                              exc_info=True, stack_info=True)
            return None

    def get_tide(self, port_id: str, date: date) -> Optional[Tide]:
        query: Query = Tide.query
        try:
            tide: LCTide = query.equal_to(Tide.PORT, port_id)\
                .equal_to(Tide.DATE, date)\
                .include(Port.__name__)\
                .first()
            return Tide()
        except Exception as ex:
            self.logger.error(f"get tide {port_id}/{date} failed. {ex}",
                              exc_info=True, stack_info=True)
            return None

    def get_all_areas(self) -> List[AreaInfo]:
        return super().get_all_areas()

    def get_all_ports(self) -> List[PortInfo]:
        return super().get_all_ports()
