"""Common definitions for DAO."""

from enum import Enum, auto


class ExecState(Enum):
    """Execute result"""
    # execute successfully
    SUCCESS = auto()
    # record already exists
    EXIST = auto()
    # record does not exist
    UN_EXIST = auto()
    # execute failed
    FAIL = auto()
    # create record successfully
    CREATE = auto()
    # update record successfully
    UPDATE = auto()
    # delete record successfully
    DELETE = auto()
