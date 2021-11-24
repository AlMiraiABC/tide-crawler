from typing import _T, Type


class Singleton(object):
    _instance = None

    def __new__(cls: Type[_T]) -> _T:
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()
