import datetime
from typing import List, Optional

from config import CRAWLER, Crawlers
from storages.model import Area, Port, Province, Tide
from utils.meta import merge_meta
from utils.singleton import Singleton

from services.basecrawlerservice import BaseCrawlerService
from services.nmdis_service import NmdisService


class CrawlerService(merge_meta(BaseCrawlerService, Singleton)):
    def __init__(self) -> None:
        super().__init__()
        if CRAWLER == Crawlers.NMDIS:
            self.service = NmdisService()
            self.set_up()
        else:
            raise NotImplemented('CRAWLER must be Crawlers.')

    def set_up(self):
        return self.service.set_up()

    def __del__(self):
        return self.tear_down()

    def tear_down(self):
        return self.service.tear_down()

    async def crawl_areas(self) -> List[Area]:
        return await self.service.crawl_areas()

    async def crawl_area(self, area_id: str) -> Optional[Area]:
        return await self.service.crawl_area(area_id)

    async def crawl_provinces(self, area_id: str) -> Optional[Province]:
        return await self.service.crawl_provinces(area_id)

    async def crawl_province(self, province_id: str) -> List[Province]:
        return await self.service.crawl_province(province_id)

    async def crawl_ports(self, province_id: str) -> List[Port]:
        return await self.service.crawl_ports(province_id)

    async def crawl_port(self, port_id: str) -> Optional[Port]:
        return await self.service.crawl_port(port_id)

    async def crawl_tide(self, d: datetime.date, port_id: str) -> Optional[Tide]:
        return await self.service.crawl_tide(d, port_id)
