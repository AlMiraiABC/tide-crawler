"""Common definitions for DAO."""

from enum import Enum, auto


class ExecState(Enum):
    """Execute result"""
    # execute successfully, used for CRD
    SUCCESS = auto()
    # record already exists, used for C
    EXIST = auto()
    # record does not exist, used for D
    UN_EXIST = auto()
    # execute failed, used for CRD
    FAIL = auto()
    CREATE = auto()
    UPDATE = auto()
    DELETE = auto()
