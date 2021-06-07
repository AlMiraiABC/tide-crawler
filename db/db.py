from enum import Enum, auto

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import DatabaseSetting


class ExecState(Enum):
    """执行结果的状态"""
    # 成功，用于CRD
    SUCCESS = auto()
    # 已存在，用于C
    EXIST = auto()
    # 不存在，用于D
    UN_EXIST = auto()
    # 失败，用于CRD
    FAIL = auto()


class DbUtil:
    """
    util for database to manage connections/sessions
    """
    def __init__(self,
                 host: str = DatabaseSetting.HOST,
                 port: int = DatabaseSetting.PORT,
                 username: str = DatabaseSetting.USERNAME,
                 password: str = DatabaseSetting.PASSWORD,
                 database: str = DatabaseSetting.DATABASE):
        """
        init database connection, create engine and sessionFactory.
        Please use :class:`DatabaseSetting` to set params
        """
        self._engine_str = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
        self.engine = create_engine(self._engine_str)
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
