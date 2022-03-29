from typing import Iterable, List, Tuple, Union


class Value:
    @staticmethod
    def is_any_none_or_empty(values: Iterable) -> bool:
        """
        是否存在至少一个值为 ``None`` 或 ``空`` 或 ``False``

        :param values: 多个值
        :return: 存在则返回 ``True``，否则返回 ``False``
        """
        for v in values:
            if not v:
                return True
        return False

    @staticmethod
    def is_null_or_whitespace(*args: str) -> bool:
        """
        Determine whether at leaset one argument is `None` or only contains blanks.

        Examples:
        -----------

        >>> is_null_or_whitespace('') # True
        >>> is_null_or_whitespace('  ') # True
        >>> is_null_or_whitespace(None) # Talse
        >>> is_null_or_whitespace('abc') # False
        >>> is_null_or_whitespace(['', 'abc']) # True
        >>> is_null_or_whitespace(['  ', 'abc']) # True
        >>> is_null_or_whitespace(['abc','def']) # False
        """
        for v in args:
            if not v or not v.strip():
                return True
