from datetime import date

from aiohttp import web
from aiohttp.web import Request
from cache.cache_util import CacheUtil
from storages.basedbutil import IDT

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


@routes.get('/area/{id}')
# @alru_cache
async def get_area(request: Request):
    pid = request.match_info.get('id')
    area = await CacheUtil().get_area(pid, IDT.ID)
    return wrap_response(to_area_model(area))


@routes.get('/province/{id}')
# @alru_cache
async def get_province(request: Request):
    pid = request.match_info.get('id')
    province = await CacheUtil().get_province(pid, IDT.ID)
    return wrap_response(to_province_model(province))


@routes.get('/port/{id}')
# @alru_cache
async def get_port(request: Request):
    pid = request.match_info.get('id')
    port = await CacheUtil().get_port(pid, IDT.ID)
    return wrap_response(to_port_model(port))


@routes.get('/tide/{port}/{date}')
# @alru_cache
async def get_tide(request: Request):
    port_id = request.match_info.get('port')
    date_str = request.match_info.get('date')
    try:
        d = date.fromisoformat(date_str)
        tide = await CacheUtil().get_tide(port_id, d)
        return wrap_response(to_tide_model(tide))
    except:
        return web.Response(status=400, reason='malformat date, must be iso format: yyyy-MM-dd')
