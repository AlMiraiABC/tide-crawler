class Value:
    @staticmethod
    def is_any_none_or_empty(*values: any) -> bool:
        """
        是否存在至少一个值为 ``None``, ``False``, ``0`` 等可表示为``False``的对象

        :param values: 多个值
        :return: 存在则返回 ``True``，否则返回 ``False``
        """
        for v in values:
            if not v:
                return True
        return False

    @staticmethod
    def is_any_none_or_whitespace(*args: str) -> bool:
        """
        Determine whether at leaset one argument is `None` or only contains blanks.

        Examples:
        -----------

        >>> Value.is_any_none_or_whitespace('') # True
        >>> Value.is_any_none_or_whitespace('  ') # True
        >>> Value.is_any_none_or_whitespace(None) # True
        >>> Value.is_any_none_or_whitespace('abc') # False
        >>> Value.is_any_none_or_whitespace('', 'abc') # True
        >>> Value.is_any_none_or_whitespace('  ', 'abc') # True
        >>> Value.is_any_none_or_whitespace('abc','def') # False
        """
        for v in args:
            if isinstance(v, str):
                if not v or not v.strip():
                    return True
            if not v:
                return True
        return False
