from unittest import TestCase
from utils.singleton import Singleton


class _SingletonClass(Singleton):
    def __init__(self, *args, **kwargs) -> None:
        pass


class TestSingleton(TestCase):
    def test_id_equal(self):
        i1 = _SingletonClass()
        i2 = _SingletonClass()
        self.assertEqual(id(i1), id(i2))

    def test_id_equal_with_arg(self):
        i1 = _SingletonClass(1, 2)
        i2 = _SingletonClass(x=1, y=2)
        self.assertEqual(id(i1), id(i2))
