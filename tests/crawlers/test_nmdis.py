from datetime import datetime
from unittest import IsolatedAsyncioTestCase, TestCase

from crawlers.nmdis import Nmdis


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
    """Get infos from nmdis to verify the links, do not mock requests."""
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.nmdis = Nmdis()

    async def test_get_tide(self):
        DATE = datetime.today().date()
        PORT_CODE = 'T020'  # Qinhuangdao
        tide = await self.nmdis.get_tide(PORT_CODE, DATE)
        self.assertIsNotNone(tide)
        self.assertEquals(len(tide.day), 24)
        self.assertEquals(tide.date.date(), DATE)

    async def test_get_provinces(self):
        AREA_CODE = '5010464519851424942'  # China Offshore Areas
        provinces = await self.nmdis.get_provinces(AREA_CODE)
        # China has 9 provinces, 1 autonomous-regions(Guangxi), 2 municipality(Tianjin, Shanghai)
        self.assertEquals(len(provinces), 12)

    async def test_get_ports(self):
        PROVINCE_CODE = '4975833679728738945'  # Hebei
        ports = await self.nmdis.get_ports(PROVINCE_CODE)
        self.assertGreater(len(ports), 0)

    async def test_get_areas(self):
        areas = await self.nmdis.get_areas()
        self.assertGreater(len(areas), 0)
