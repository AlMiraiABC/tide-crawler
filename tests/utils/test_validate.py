from unittest import TestCase

from utils.validate import Value


class TestValue(TestCase):
    def test_is_any_none_or_empty(self):
        vs = [{"abc": 123}, {1, 2, 3}, (1, 2), ['a']]
        self.assertFalse(Value.is_any_none_or_empty(*vs))
        self.assertTrue(Value.is_any_none_or_empty(*vs, None))
        self.assertTrue(Value.is_any_none_or_empty(*vs, ''))
        self.assertTrue(Value.is_any_none_or_empty(*vs, 0))
        self.assertTrue(Value.is_any_none_or_empty(*vs, {}))

    def test_is_any_none_or_whitespace(self):
        vs = ['abc', '123']
        self.assertTrue(Value.is_any_none_or_whitespace(*vs, ''))
        self.assertTrue(Value.is_any_none_or_whitespace(*vs, '  '))
        self.assertTrue(Value.is_any_none_or_whitespace(*vs, None))
        self.assertFalse(Value.is_any_none_or_whitespace(*vs, 'abc'))
