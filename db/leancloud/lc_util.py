
from leancloud.errors import LeanCloudError
from leancloud.query import Query
from config import LCSetting
from crawler.model.location import AreaInfo, PortInfo
from db.common import ExecState
from db.dbutil import BaseDbUtil
from db.leancloud.model import Area, Port

import leancloud

from db.tide import TideDay, TideInfo, TideLimit


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
        id = LCSetting.APP_ID
        key = LCSetting.APP_KEY if LCSetting.APP_KEY else LCSetting.MASTER_KEY
        leancloud.init(id, key)
        self.login()

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
            exist = query.equal_to(Area.NAME, area.name).first()
            save()
        except LeanCloudError as ex:
            if ex.code == 101:
                # region add new record
                exist = AreaInfo()
                save()
                return
                # endregion
            raise ex

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
            save()
            return ExecState.CREATE
        except LeanCloudError as ex:
            if ex.code == 101:
                exist = PortInfo()
                save()
                return ExecState.UPDATE
            return ExecState.FAIL

    def add_tide(self, info: TideInfo, day: TideDay, limit: TideLimit) -> ExecState:
        return super().add_tide(info, day, limit)
