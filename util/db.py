from enum import Enum, auto

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import Config


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
    def __init__(self,
                 host: str = Config.HOST,
                 port: int = Config.PORT,
                 username: str = Config.USERNAME,
                 password: str = Config.PASSWORD,
                 database: str = Config.DATABASE):
        self._engine_str = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
        self.engine = create_engine(self._engine_str)
        self.sessionFactory = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        return self.sessionFactory()

    @staticmethod
    def close_session(session: Session) -> ExecState:
        try:
            session.commit()
            return ExecState.SUCCESS
        except:
            session.rollback()
            return ExecState.FAIL
        finally:
            session.close()


db_util = DbUtil()
