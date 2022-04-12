from datetime import datetime
from typing import List, Optional
from config import CRAWLER, Crawlers
from db.model import Area, Port, Province
from service.basecrawlerservice import BaseCrawlerService
from service.nmdis_service import NmdisService


class CrawlerService(BaseCrawlerService):
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

    async def get_areas(self) -> List[Area]:
        return await self.service.get_areas()

    async def get_area(self, area_id: str) -> Optional[Area]:
        return await self.service.get_area(area_id)

    async def get_provinces(self, area_id: str) -> Optional[Province]:
        return await self.service.get_provinces(area_id)

    async def get_province(self, province_id: str) -> List[Province]:
        return await self.service.get_province(province_id)

    async def get_ports(self, province_id: str) -> List[Port]:
        return await self.service.get_ports(province_id)

    async def get_port(self, port_id: str) -> Port:
        return await self.service.get_port(port_id)

    async def get_tide(self, port_id: str, d: datetime.date) -> Optional[Tide]:
        return await self.service.get_tide(port_id, d)

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
