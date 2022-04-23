import json
from datetime import date, time
from typing import Any, Callable, Union
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import patch

from crawlers.nmdis import Nmdis
from storages.model import TideItem


class TestNmdis(TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.nmdis = Nmdis()

    def test__get_datum(self):
        result = self.nmdis._get_datum('在平均海面下241cm')
        self.assertEqual(result, -241)

    def test__get_tide_data(self):
        data = {
            "a11": 165.0,
            "cs1": "09:54",
            "a10": 143.0,
            "cs0": "03:37",
            "cg1": 142.0,
            "cg0": 338.0,
            "otherkey": "balabala"
        }
        day, limit = self.nmdis._get_tide_data(data)
        DAY = [TideItem(time(11), 165.0), TideItem(time(10), 143.0)]
        LIMIT = [TideItem(time(9, 54), 142.0), TideItem(time(3, 37), 338.0)]
        self.assertListEqual([d.to_dict()for d in day],
                             [d.to_dict() for d in DAY])
        self.assertListEqual([l.to_dict() for l in limit],
                             [l.to_dict() for l in LIMIT])


GET_MODEL = 'aiohttp.ClientSession.get'


class TestNmdisAsync(IsolatedAsyncioTestCase):
    """Get infos from nmdis to verify the links, do not mock requests."""

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.nmdis = Nmdis()

    def mock_client(self, m, status: int = 200, **kwargs: Union[Any, Callable[[], Any]]):
        mresp = m.return_value.__aenter__.return_value
        mresp.status = status
        for k, v in kwargs.items():
            if callable(v):
                setattr(getattr(mresp, k), 'return_value', v())
            else:
                setattr(mresp, k, v)
        return m

    @patch(GET_MODEL)
    async def test_get_areas(self, get):
        RID = '5010464519851424942'
        NAME = '中国近海海域'
        mock_data = {
            "success": True,
            "msg": "信息操作成功!",
            "data": [
                {
                    "page": 1,
                    "pageSize": 20,
                    "total": 0,
                    "totalPage": 1,
                    "sort": None,
                    "order": None,
                    "id": RID,
                    "recordtime": "2017-01-12 13:56:58",
                    "areaname": NAME,
                    "areaenname": "China Offshore Areas",
                    "pyname": "",
                    "parentid": "0",
                    "levelid": 0,
                    "sortindex": 0
                }
            ]
        }
        self.mock_client(get, json=lambda: mock_data,
                         text=lambda: json.dumps(mock_data))
        areas = await self.nmdis.get_areas()
        self.assertEquals(len(areas), 1)
        self.assertEquals(areas[0].rid, RID)
        self.assertEquals(areas[0].name, NAME)

    @patch(GET_MODEL)
    async def test_get_provinces(self, get):
        RID = '5359678358229842731'
        ARID = '5010464519851424942'
        NAME = '福建'
        mock_data = {
            "success": True,
            "msg": "信息操作成功!",
            "data": [
                {
                    "page": 1,
                    "pageSize": 20,
                    "total": 0,
                    "totalPage": 1,
                    "sort": None,
                    "order": None,
                    "id": RID,
                    "recordtime": "2017-01-12 13:56:58",
                    "areaname": NAME,
                    "areaenname": "Fujian",
                    "pyname": "",
                    "parentid": ARID,
                    "levelid": 1,
                    "sortindex": 7
                }
            ]
        }
        self.mock_client(get, json=lambda: mock_data,
                         text=lambda: json.dumps(mock_data))
        provinces = await self.nmdis.get_provinces(ARID)
        self.assertEquals(len(provinces), 1)
        self.assertEquals(provinces[0].rid, RID)
        self.assertEquals(provinces[0].name, NAME)
        self.assertEquals(provinces[0].area.rid, ARID)

    @patch(GET_MODEL)
    async def test_get_provinces_no_data(self, get):
        mock_data = {
            "success": True,
            "msg": "信息操作成功!",
            "data": [],
            "page": None,
            "attr": {}
        }
        self.mock_client(get, json=lambda: mock_data,
                         text=lambda: json.dumps(mock_data))
        provinces = await self.nmdis.get_provinces('abcdefg')
        self.assertListEqual(provinces, [])

    @patch(GET_MODEL)
    async def test_get_ports(self, get):
        PRID = '4975833679728738945'
        RID = 'T025'
        NAME = '岐口'
        GEO = (38.6, 117.51666667)
        mock_data = {
            "success": True,
            "msg": "",
            "data": [
                {
                    "page": 1,
                    "pageSize": 20,
                    "total": 0,
                    "totalPage": 1,
                    "sort": None,
                    "order": None,
                    "id": "4613335436031122682",
                    "recordtime": "2017-05-18 09:29:18",
                    "state": 1,
                    "code": RID,
                    "name": NAME,
                    "enname": "QIKOU",
                    "pyname": "QK",
                    "coordx": GEO[1],
                    "coordy": GEO[0],
                    "datatype": 1,
                    "areaid": PRID
                },
            ]
        }
        self.mock_client(get, json=lambda: mock_data,
                         text=lambda: json.dumps(mock_data))
        ports = await self.nmdis.get_ports(PRID)
        self.assertEquals(len(ports), 1)
        self.assertEquals(ports[0].rid, RID)
        self.assertEquals(ports[0].name, NAME)
        self.assertEquals(ports[0].province.rid, PRID)
        self.assertEquals(ports[0].geopoint, GEO)

    @patch(GET_MODEL)
    async def test_get_ports_no_data(self, get):
        mock_data = {
            "success": True,
            "msg": "",
            "data": [],
            "page": {
                "page": 1,
                "pageSize": 20,
                "total": 0,
                "totalPage": 1,
                "sort": None,
                "order": None
            },
            "attr": {}
        }
        self.mock_client(get, json=lambda: mock_data,
                         text=lambda: json.dumps(mock_data))
        ports = await self.nmdis.get_ports('abcdefg')
        self.assertListEqual(ports, [])

    @patch(GET_MODEL)
    async def test_get_tide(self, get):
        PRID = 'T020'
        DATE = date(2022, 4, 7)
        DATUM = -91
        mock_data = {
            "success": True,
            "msg": "",
            "data": [
                {
                    "page": 1,
                    "pageSize": 20,
                    "total": 0,
                    "totalPage": 1,
                    "sort": None,
                    "order": None,
                    "id": "c0646ce5ca984f8d9bd945db3fe60fb2",
                    "recordtime": "2021-10-12 15:54:10",
                    "state": "1",
                    "sitecode": PRID,
                    "title": "秦皇岛",
                    "year": "2022",
                    "month": "4",
                    "coordinate": "   39°54′N119°36′E",
                    "timearea": "-0800",
                    "benchmark": f"在平均海面{'下' if DATUM <0 else '上'}{DATUM}cm",
                    "signature": "超级管理员",
                    "filedata": {
                        "a11": 49,
                        "cs1": "23:37",
                        "RecordTime": "2021-10-12 15:54:10",
                        "a10": 39,
                        "cs0": "09:00",
                        "a13": 64,
                        "a12": 59,
                        "a15": 81,
                        "a14": 70,
                        "a17": 95,
                        "a16": 92,
                        "a19": 95,
                        "ReportID": "5615735777594209636",
                        "a18": 93,
                        "cg1": 138,
                        "cg0": 34,
                        "ID": "5377717703490748296",
                        "a20": 101,
                        "a22": 128,
                        "a21": 114,
                        "a23": 136,
                        "a0": 125,
                        "a1": 115,
                        "a2": 102,
                        "a3": 92,
                        "a4": 87,
                        "a5": 77,
                        "a6": 62,
                        "a7": 48,
                        "a8": 39,
                        "a9": 34,
                        "Day": 7
                    },
                    "serchdate": DATE.isoformat(),
                    "inserttime": "2021-11-07 23:41:56"
                }
            ]
        }
        self.mock_client(get, json=lambda: mock_data,
                         text=lambda: json.dumps(mock_data))
        tide = await self.nmdis.get_tide(PRID, DATE)
        self.assertEquals(tide.datum, DATUM)
        self.assertEquals(tide.port.rid, PRID)
        self.assertEquals(len(tide.day), 24)
        self.assertEquals(len(tide.limit), 2)

    @patch(GET_MODEL)
    async def test_get_tide_no_data(self, get):
        mock_data = {
            "success": True,
            "msg": "",
            "data": [],
            "attr": {}
        }
        self.mock_client(get, json=lambda: mock_data,
                         text=lambda: json.dumps(mock_data))
        tide = await self.nmdis.get_tide('abcde', date(2000, 1, 1))
        self.assertIsNone(tide)
