from enum import Enum, auto

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import DatabaseSetting, LeanCloudSetting
import leancloud


class ExecState(Enum):
    """execute result"""
    # execute successfully, used for CRD
    SUCCESS = auto()
    # record already exists, used for C
    EXIST = auto()
    # record does not exist, used for D
    UN_EXIST = auto()
    # execute failed, used for CRD
    FAIL = auto()


class DbUtil:
    """
    util for database to manage connections/sessions
    """

    def __init__(self, **kwargs):
        """
        init database connection, create engine and sessionFactory.

        Please use :class:`DatabaseSetting` to set params

        See also
        ------
        https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls
        """
        dialect: str = DatabaseSetting.DIALECT or 'mysql'
        driver: str = '+'+DatabaseSetting.DRIVER if DatabaseSetting.DRIVER else ''
        host: str = DatabaseSetting.HOST or 'localhost'
        port: str = ':'+DatabaseSetting.PORT if DatabaseSetting.PORT else ''
        username: str = DatabaseSetting.USERNAME or 'root'
        password: str = DatabaseSetting.PASSWORD or 'root'
        database: str = DatabaseSetting.DATABASE or 'tide'
        self._engine_str = f'{dialect}{driver}://{username}:{password}@{host}{port}/{database}'
        self.engine = create_engine(
            self._engine_str, **DatabaseSetting.KWARGS, **kwargs)
        self.sessionFactory = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        """get a session"""
        return self.sessionFactory()

    @staticmethod
    def close_session(session: Session) -> ExecState:
        """
        commit or rollback(commit failed) and then close this session,

        :return: :class:`ExecState.SUCCESS` if commit success, or else rollback and return :class:`ExecState.FAIL`
        """
        # noinspection PyBroadException
        try:
            session.commit()
            return ExecState.SUCCESS
        except Exception:
            session.rollback()
            return ExecState.FAIL
        finally:
            session.close()


db_util = DbUtil()


class LCUtil:
    """
    util for LeanCloud
    """

    def __init__(self) -> None:
        """
        create connection to leancloud data storage and login with config

        Please use :class:`LeanCloudSetting` to set params

        See also
        ------
        https://leancloud.cn/docs/sdk_setup-python.html#hash20935048
        """
        id = LeanCloudSetting.APP_ID
        key = LeanCloudSetting.APP_KEY if LeanCloudSetting.APP_KEY else LeanCloudSetting.MASTER_KEY
        leancloud.init(id, key)
        self.login()

    def login(username=LeanCloudSetting.SPIDER_USERNAME, password=LeanCloudSetting.SPIDER_PASSWORD) -> None:
        """
        login with a special User which has auths to create, delete, find, get, update

        See also
        ------
        https://leancloud.cn/docs/leanstorage_guide-python.html#hash964666
        """
        user = leancloud.User()
        user.login(username, password)

    def logout() -> None:
        """
        logout current User. Use :function:`LCUtil.login` to re-login

        See also
        ------
        https://leancloud.cn/docs/leanstorage_guide-python.html#hash748191977
        """
        user = leancloud.User.get_current()
        user and user.logout()
