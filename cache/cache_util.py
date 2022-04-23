from typing import Type
from storages.basedbutil import BaseDbUtil
from storages.dbutil import DbUtil
from utils.meta import merge_meta
from utils.singleton import Singleton


class CacheUtil(merge_meta(BaseDbUtil, Singleton)):

    def __new__(cls: Type[DbUtil]) -> DbUtil:
        return DbUtil()
