from datetime import date

from aiohttp import web
from aiohttp.web_request import Request

from cache.cache_util import CacheUtil
from storages.basedbutil import IDT

app = web.Application()

routes = web.RouteTableDef()


@routes.get('/list/areas')
async def get_areas(_):
    return web.json_response(await CacheUtil().get_areas())


@routes.get('/list/provinces/{area}')
async def get_provinces(request: Request):
    area_id = request.match_info.get('area')
    return web.json_response(await CacheUtil().get_provinces(area_id, IDT.ID))


@routes.get('/list/ports/{province}')
async def get_ports(request: Request):
    province_id = request.match_info.get('province')
    return web.json_response(await CacheUtil().get_provinces(province_id, IDT.ID))


@routes.get('/area/{id}')
async def get_area(request: Request):
    pid = request.match_info.get('id')
    return web.json_response(await CacheUtil().get_area(pid, IDT.ID))


@routes.get('/province/{id}')
async def get_province(request: Request):
    pid = request.match_info.get('id')
    return web.json_response(await CacheUtil().get_province(pid, IDT.ID))


@routes.get('/port/{id}')
async def get_port(request: Request):
    pid = request.match_info.get('id')
    return web.json_response(await CacheUtil().get_port(pid, IDT.ID))


@routes.get('/tide/{port}/{date}')
async def get_tide(request: Request):
    port_id = request.match_info.get('port')
    date_str = request.match_info.get('date')
    try:
        d = date.fromisoformat(date_str)
        return web.json_response(await CacheUtil().get_tide(port_id, d))
    except:
        return web.Response(status=400, reason='malformat date, must be iso format: yyyy-MM-dd')

app.add_routes(routes)
web.run_app(app)
