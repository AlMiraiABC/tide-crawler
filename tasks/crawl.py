import asyncio
import sys
from datetime import date
from typing import Callable, Coroutine, List, Optional, Tuple, TypeVar, Union

from services.crawler_service import CrawlerService
from storages.basedbutil import IDT
from storages.common import ExecState
from storages.dbutil import DbUtil
from storages.model import Tide, WithInfo
from utils.logger import Logger

_T = TypeVar('_T', bound=WithInfo)

_logger = Logger('crawl').logger


async def inserts(os: List[_T], save: Callable[[_T], Coroutine[None, None, Tuple[ExecState, Union[Optional[_T], Exception]]]]):
    ret: List[Tuple[ExecState, Union[Optional[_T], Exception]]] = []
    for o in os:
        (r, obj) = await save(o)
        ret.append((r, obj))
        if isinstance(obj, WithInfo):
            _logger.info(f'{r.name} {type(obj).__name__}({obj.objectId})')
        else:
            _logger.error(f'{r.name} {o.rid} {obj}', exc_info=obj)
    return ret


async def crawl_areas():
    areas = await CrawlerService().crawl_areas()
    return await inserts(areas, lambda o: DbUtil().add_area(o, IDT.RID))


async def crawl_provinces(area: str):
    provinces = await CrawlerService().crawl_provinces(area)
    return await inserts(provinces, lambda o: DbUtil().add_province(o, IDT.RID))


async def crawl_ports(province: str):
    ports = await CrawlerService().crawl_ports(province)
    return await inserts(ports, lambda o: DbUtil().add_port(o, IDT.RID))


async def crawl_tide(d: date, port: str):
    tide = await CrawlerService().crawl_tide(d, port)
    (ret, obj) = await DbUtil().add_tide(tide, IDT.RID)
    if isinstance(obj, Tide):
        _logger.info(f'{ret.name} {type(obj)}({obj.objectId})')
    else:
        _logger.error(f'{ret.name} {port}/{d.isoformat()} {obj}', exc_info=obj)
    return (ret, obj)


def main(args: List[str]):
    HELP = 'area\nprovince area_rid\nport province_rid\ntide yyyy-MM-dd port_rid'
    if not args:
        print(HELP)
        return
    args = args+[None, None, None]
    loop = asyncio.get_event_loop()
    op = args[0]
    if op == 'area':
        return loop.run_until_complete(crawl_areas())
    if op == 'province':
        if not args[1]:
            print(HELP)
            return
        return loop.run_until_complete(crawl_provinces(args[1]))
    if op == 'port':
        if not args[1]:
            print(HELP)
            return
        return loop.run_until_complete(crawl_ports(args[1]))
    if op == 'tide':
        if not args[1] or not args[2]:
            print(HELP)
            return
        try:
            d = date.fromisoformat(args[1])
        except:
            print('malformed date, must be yyyy-MM-dd.')
            print(HELP)
            return
        return loop.run_until_complete(crawl_tide(d, args[2]))
    print(HELP)


if __name__ == '__main__':
    main(sys.argv[1:])
