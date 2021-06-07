from typing import List

from service import ContinentService, CountryService
from crawler.selector import Selector


class Work:
    @staticmethod
    def crawl_selector():
        """
        获取从官网获取查询潮汐数据时所需的信息

        * 包括 ``country``、``port``、``province``、``china_port``

        * ``continent`` 无需获取，可直接从数据库修改
        """
        continents: List[Continent] = ContinentService.get_all_continent()
        if not continents:
            return
        for continent in continents:
            countries_name:List[str] = Selector.get_countries(continent.name)
            if not countries_name:
                return
            countries = [Country(name=country_name) for country_name in countries_name]
            countries_success,countries_exist,countries_fail = CountryService.insert_many(countries)
            print()