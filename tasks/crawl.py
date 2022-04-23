import asyncio
import sys
from datetime import date
from typing import Callable, Awaitable, List, Optional, Tuple, TypeVar, Union

from services.crawler_service import CrawlerService
from storages.basedbutil import IDT
from storages.common import ExecState
from storages.dbutil import DbUtil
from storages.model import Area, Port, Province, Tide, WithInfo
from utils.console import Console
from utils.logger import Logger

_T = TypeVar('_T', bound=WithInfo)

_logger = Logger('crawl').logger


async def inserts(os: List[_T], save: Callable[[_T], Awaitable[Tuple[ExecState, Union[Optional[_T], Exception]]]]):
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


async def crawl_init():
    areas = []
    provinces = []
    ports = []
    areas = await crawl_areas()
    err_a = []
    err_p = []
    err_po = []
    for aret, area in areas:
        if isinstance(area, Area):
            provinces = await crawl_provinces(area.rid)
            for pret, province in provinces:
                if isinstance(province, Province):
                    ports = await crawl_ports(province.rid)
                    for poret, port in ports:
                        if not isinstance(port, Port):
                            err_po.area((poret, port))
                else:
                    err_p.append((pret, province))
        else:
            err_a.append((aret, area))

    def p(rets):
        for r, obj in rets:
            Console.print_warn(f'{r.name} {obj}')
    if err_a:
        Console.print_err(f'occured erros when get areas')
        p(err_a)
    if err_p:
        Console.print_err(f'occured erros when get provinces')
        p(err_p)
    if err_po:
        Console.print_err(f'occured erros when get ports')
        p(err_po)
    return (areas, err_a), (provinces, err_p), (ports, err_po)


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
    if op == 'init':
        Console.print_warn(
            "WARNING: This will crawl all areas, provinces and ports. It may blocked your IP.")
        confirm = input('Enter y/Y to continue: ')
        if confirm.upper() in ['Y', 'YES']:
            return loop.run_until_complete(crawl_init())
        else:
            print('Canceled.')
            return
    print(HELP)


if __name__ == '__main__':
    main(sys.argv[1:])
