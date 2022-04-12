from datetime import datetime
from typing import List, NoReturn, Optional

from crawlers.nmdis import Nmdis
from storages.model import Area, Port, Province, Tide

from service.basecrawlerservice import BaseCrawlerService


class NmdisService(BaseCrawlerService):
    def __init__(self) -> None:
        super().__init__()
        self.nmdis = Nmdis()

    async def crawl_areas(self) -> List[Area]:
        """Crawls all areas"""
        return await self.nmdis.get_areas()

    async def crawl_area(self, area_id: str) -> NoReturn:
        """
        Crawls a area by area's id.
        """
        raise NotImplemented()

    async def crawl_provinces(self, area_id: str) -> Optional[Province]:
        """Crawls all provinces which belongs to specified area by area's id."""
        return await self.nmdis.get_provinces(area_id)

    async def crawl_province(self, province_id: str) -> NoReturn:
        """crawls a province by province's id."""
        raise NotImplemented()

    async def crawl_ports(self, province_id: str) -> List[Port]:
        """Crawls all ports which belgongs to specified province by province's id."""
        return await self.nmdis.get_ports(province_id)

    async def crawl_port(self, port_id: str) -> NoReturn:
        """Crawls a port by port's id."""
        raise NotImplemented()

    async def crawl_tide(self, d: datetime.date, port_id: str) -> Optional[Tide]:
        """Crawls the tide of the specified date():param:`d`) from :param:`port_id`"""
        return await self.nmdis.get_tide(port_id, d)
