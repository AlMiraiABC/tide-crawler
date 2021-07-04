import logging
from typing import List, Union


class RangeLevelFilter(logging.Filter):
    """subclass of :class:``Filter`` that allow the list of customized levelnos"""

    def __init__(self, level: Union[int, List[int]], name: str = '') -> None:
        """
        create a :class:``SingleLevelFilter`` instance

        :param level: levelno or list of levelno. such as ``logging.DEBUG``, ``logging.INFO`` ...
        :param name: see also ``logging.Filter#__init__``
        """
        super().__init__(name=name)
        self.level = level if isinstance(level, list) else [level]

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno in self.level
