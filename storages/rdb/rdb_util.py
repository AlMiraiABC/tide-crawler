from config import RDBSetting
from storages.common import ExecState
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class RDBUtil:
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
        dialect: str = self.__verify_nonnone(
            self, RDBSetting.DIALECT, "DatabaseSetting.DIALECT", False)
        driver: str = '+' + \
            self.__verify_nonnone(RDBSetting.DRIVER,
                                  "DatabaseSetting.DRIVER", True, '')
        host: str = RDBSetting.HOST or 'localhost'
        port: int = ':'+RDBSetting.PORT if RDBSetting.PORT else ''
        username: str = RDBSetting.USERNAME or 'root'
        password: str = RDBSetting.PASSWORD or 'root'
        database: str = RDBSetting.DATABASE or 'tide'
        self._engine_str = f'{dialect}{driver}://{username}:{password}@{host}{port}/{database}'
        self.engine = create_engine(
            self._engine_str, **RDBSetting.KWARGS, **kwargs)
        self.sessionFactory = sessionmaker(bind=self.engine)
        self.session: Session = self.sessionFactory()

    def __verify_nonnone(self, d: str, name: str, empty: bool = True, default: str = '') -> str:
        """
        Determine whether :param:`d` is none or :param:`empty`

        :param d: Value
        :param empty: Allow empty
        :param name: Variable name
        :param default: Default value if :param:`empty` is `True`.
        :return: :param:`d` or :param:`default` if valid or else throw
        """
        if d is None:
            raise ValueError(f"{name} must be a Non-None value")
        if empty:
            if d:
                return d
            else:
                return default
        else:
            if not d or d.isspace():
                raise ValueError(f"{name} must be a Non-Empty value")
        return d

    def open(self) -> Session:
        """Get a session"""
        if not self.session.is_active:
            self.session = self.sessionFactory()
        return self.session

    def close(self) -> ExecState:
        """
        Commit or rollback(commit failed) and then close this session,

        :return: :class:`ExecState.SUCCESS` if commit success, or else rollback and return :class:`ExecState.FAIL`
        """
        if not self.session.is_active:
            return ExecState.SUCCESS
        try:
            self.session.commit()
            return ExecState.SUCCESS
        except Exception:
            self.session.rollback()
            return ExecState.FAIL
        finally:
            self.session.close()
