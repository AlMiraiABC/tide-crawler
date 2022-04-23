from datetime import date

from aiohttp import web
from aiohttp.web import Request
from cache.cache_util import CacheUtil
from services.crawler_service import CrawlerService
from storages.basedbutil import IDT
from storages.dbutil import DbUtil

from web.model import (to_area_model, to_models, to_port_model,
                       to_province_model, to_tide_model, wrap_response)

routes = web.RouteTableDef()


@routes.get('/list/areas')
# @alru_cache # TODO: type Request is unhashtable
async def get_areas(_):
    areas = await CacheUtil().get_areas()
    return wrap_response(to_models(areas, to_area_model))


@routes.get('/list/provinces/{area}')
# @alru_cache
async def get_provinces(request: Request):
    area_id = request.match_info.get('area')
    provinces = await CacheUtil().get_provinces(area_id, IDT.ID)
    return wrap_response(to_models(provinces, to_province_model))


@routes.get('/list/ports/{province}')
# @alru_cache
async def get_ports(request: Request):
    province_id = request.match_info.get('province')
    ports = await CacheUtil().get_ports(province_id, IDT.ID)
    return wrap_response(to_models(ports, to_port_model))


def resp404(obj):
    return web.Response(status=404, reason=f'{obj} doesn\'t exist.')


@routes.get('/area/{id}')
# @alru_cache
async def get_area(request: Request):
    pid = request.match_info.get('id')
    area = await CacheUtil().get_area(pid, IDT.ID)
    if area is None:
        return resp404(f'area: {pid}')
    return wrap_response(to_area_model(area))


@routes.get('/province/{id}')
# @alru_cache
async def get_province(request: Request):
    pid = request.match_info.get('id')
    province = await CacheUtil().get_province(pid, IDT.ID)
    if province is None:
        return resp404(f'province: {pid}')
    return wrap_response(to_province_model(province))


@routes.get('/port/{id}')
# @alru_cache
async def get_port(request: Request):
    pid = request.match_info.get('id')
    port = await CacheUtil().get_port(pid, IDT.ID)
    if port is None:
        return resp404(f'port: {pid}')
    return wrap_response(to_port_model(port))


@routes.get('/tide/{port}/{date}')
# @alru_cache
async def get_tide(request: Request):
    port_id = request.match_info.get('port')
    date_str = request.match_info.get('date')
    try:
        d = date.fromisoformat(date_str)
    except:
        return web.Response(status=400, reason='malformat date, must be iso format: yyyy-MM-dd')
    tide = await CacheUtil().get_tide(port_id, d)
    if tide is None:
        port = await DbUtil().get_port(port_id, IDT.ID)
        if port is None:
            return web.Response(status=404, reason=f'cannot found port: {port_id}')
        tide = await CrawlerService().crawl_tide(d, port.rid)
        await DbUtil().add_tide(tide, IDT.RID)
    return wrap_response(to_tide_model(tide))
