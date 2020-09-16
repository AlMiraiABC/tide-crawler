from typing import Iterable


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
