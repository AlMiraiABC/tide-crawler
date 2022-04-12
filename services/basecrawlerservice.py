import datetime
from abc import ABC, abstractmethod
from typing import List, Optional

from storages.basedbutil import IDT
from storages.dbutil import DbUtil
from storages.model import Area, Port, Province, Tide


class BaseCrawlerService(ABC):
    """Based services for crawlers. A common interface to using crawlers."""

    def __init__(self) -> None:
        super().__init__()
        self.set_up()

    def __del__(self):
        self.tear_down()

    def set_up(self):
        """Initialize."""
        pass

    def tear_down(self):
        """Destory."""
        pass

    @abstractmethod
    async def crawl_areas(self) -> List[Area]:
        """Crawls all areas"""
        pass

    @abstractmethod
    async def crawl_area(self, area_id: str) -> Optional[Area]:
        """Crawls a area by area's id."""
        pass

    @abstractmethod
    async def crawl_provinces(self, area_id: str) -> Optional[Province]:
        """Crawls all provinces which belongs to specified area by area's id."""
        pass

    @abstractmethod
    async def crawl_province(self, province_id: str) -> List[Province]:
        """crawls a province by province's id."""
        pass

    @abstractmethod
    async def crawl_ports(self, province_id: str) -> List[Port]:
        """Crawls all ports which belgongs to specified province by province's id."""
        pass

    @abstractmethod
    async def crawl_port(self, port_id: str) -> Optional[Port]:
        """Crawls a port by port's id."""

    @abstractmethod
    async def crawl_tide(self, d: datetime.date, port_id: str) -> Optional[Tide]:
        """Crawls the tide of the specified date():param:`d`) from :param:`port_id`"""
