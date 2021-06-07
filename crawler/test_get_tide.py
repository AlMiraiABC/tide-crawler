from datetime import datetime
from unittest import TestCase

from crawler.get_tide import GetTide


class TestGetTide(TestCase):
    def test_data(self):
        limit, data, info = GetTide.data(1, datetime.now().date())
        print(str(limit))
        print(str(data))
        print(str(info))
