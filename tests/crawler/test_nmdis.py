from datetime import date
from unittest import TestCase, IsolatedAsyncioTestCase

from crawler.nmdis import Nmdis
from db.basedbutil import IDT
from db.dbutil import DbUtil


class TestNmdis(TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.nmdis = Nmdis()

    def test___get_datum(self):
        result = self.nmdis._Nmdis__get_datum('在平均海面下241cm')
        self.assertEqual(result, -241)

    def test___get_tide_data(self):
        data = {"a11": 165.0, "cs1": "09:54", "RecordTime": "2021-07-23 15:39:16", "a10": 143.0, "cs0": "03:37", "a13": 269.0, "cs3": "22:12", "a12": 214.0, "cs2": "15:07", "a15": 326.0, "a14": 309.0, "a17": 285.0, "a16": 316.0, "a19": 184.0, "ReportID": "5457026288864211009", "a18": 238.0,
                "cg1": 142.0, "cg0": 338.0, "cg3": 61.0, "cg2": 326.0, "ID": "5415271443364952074", "a20": 128.0, "a22": 62.0, "a21": 84.0, "a23": 75.0, "a0": 167.0, "a1": 239.0, "a2": 299.0, "a3": 333.0, "a4": 336.0, "a5": 318.0, "a6": 287.0, "a7": 244.0, "a8": 197.0, "a9": 157.0, "Day": 20}
        day, limit = self.nmdis._Nmdis__get_tide_data(data)
        self.assertEquals(len(day), 24)
        self.assertEqual(len(limit), 4)


class TestNmdisAsync(IsolatedAsyncioTestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.nmdis = Nmdis()

    async def test_get_tide(self):
        DATE = date(2022, 4, 4)
        tide = await self.nmdis.get_tide('T020', DATE)
        self.assertIsNotNone(tide)
        self.assertEquals(len(tide.day), 24)
        self.assertEquals(tide.date.date(), DATE)

    async def test_get_provinces(self):
        AREA_CODE = '5010464519851424942'  # China 中国近海海域
        provinces = await self.nmdis.get_provinces(AREA_CODE)
        self.assertEquals(len(provinces), 12)
        self.assertEquals
