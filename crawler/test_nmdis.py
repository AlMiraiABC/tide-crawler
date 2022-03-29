import json
from unittest import TestCase

from crawler.nmdis import Nmdis


class TestNmdis(TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.nmdis = Nmdis()

    def test___get_datum(self):
        result = self.nmdis.__get_datum('在平均海面下241cm')
        print(result)
        self.assertEqual(result, -241)

    def test___get_tide_data(self):
        text = '"data":[{"page":1,"pageSize":20,"total":0,"totalPage":1,"sort":null,"order":null,"id":"68bbbe44bebc4c0b99e17c110429fe4d","recordtime":"2021-07-23 15:39:16","state":"1","sitecode":"T024","title":"塘沽","year":"2021","month":"11","coordinate":"   38°59′N117°47′E","timearea":"-0800","benchmark":"在平均海面下241cm","signature":"超级管理员","filedata":{"a11":165.0,"cs1":"09:54","RecordTime":"2021-07-23 15:39:16","a10":143.0,"cs0":"03:37","a13":269.0,"cs3":"22:12","a12":214.0,"cs2":"15:07","a15":326.0,"a14":309.0,"a17":285.0,"a16":316.0,"a19":184.0,"ReportID":"5457026288864211009","a18":238.0,"cg1":142.0,"cg0":338.0,"cg3":61.0,"cg2":326.0,"ID":"5415271443364952074","a20":128.0,"a22":62.0,"a21":84.0,"a23":75.0,"a0":167.0,"a1":239.0,"a2":299.0,"a3":333.0,"a4":336.0,"a5":318.0,"a6":287.0,"a7":244.0,"a8":197.0,"a9":157.0,"Day":20},"serchdate":"2021-11-20","inserttime":"2021-10-30 07:37:35"}]'
        data = json.loads(text)
        day, limit = self.nmdis.__get_tide_data(data)
        print(day, limit)
        self.assertEquals(len(day), 24)
        self.assertEqual(len(limit), 4)
