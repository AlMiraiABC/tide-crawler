from typing import List


class DictConverter:
    @staticmethod
    def obj_to_dict(obj: object):
        """
        Convert :param:`obj`'s properties to dict and values convert to str

        --------
        Example:

        >>> class T:
        >>>     def __init__(a,b):
        >>>         self.a = a
        >>>         self.b = b
        >>> t=T(datetime.datetime.now(), [1,2,3])
        >>> DictConverter.obj_to_dict(t) # {'a': ''2022-01-01 22:32:49.794259', 'b': '[1,2,3]'}
        """
        d = {}
        for k, v in obj.__dict__.items():
            d[k] = str(v)
        return d

    def list_to_dict(objs: List[object]):
        return [DictConverter.obj_to_dict(obj) for obj in objs]
