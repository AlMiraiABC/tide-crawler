from datetime import datetime
from unittest import IsolatedAsyncioTestCase

from storages.common import ExecState

from tasks.crawl import crawl_areas, crawl_ports, crawl_provinces, crawl_tide


class TestCrawl(IsolatedAsyncioTestCase):
    def assertSuccess(self, rets: list):
        for (ret, _) in rets:
            self.assertIn(
                ret, [ExecState.CREATE, ExecState.UPDATE, ExecState.SUCCESS])

    async def test_crawl_areas(self):
        rets = await crawl_areas()
        self.assertSuccess(rets)

    async def test_crawl_provinces(self):
        rets = await crawl_provinces('5010464519851424942') # china
        self.assertSuccess(rets)

    async def test_crawl_ports(self):
        rets = await crawl_ports('4845586374601047334')  # zhejiang
        self.assertSuccess(rets)

    async def test_crawl_tide(self):
        (ret, _) = await crawl_tide(datetime.today().date(),'T098') # wenzhou
        self.assertIn(ret, [ExecState.CREATE, ExecState.SUCCESS])
