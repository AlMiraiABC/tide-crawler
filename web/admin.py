import json
import os
from typing import Optional, Tuple, TypedDict, Union

import bcrypt
import tasks.crawl as crawl
from aiohttp import web
from aiohttp.web import Request
from cache.dict_db import DictDb
from cache.cache_util import CacheUtil
from services.crawler_service import CrawlerService
from storages.common import ExecState
from storages.model import WithInfo

from web.constant import ErrCode
from web.model import wrap_response

routes = web.RouteTableDef()


class AdminConfigDict(TypedDict):
    users: dict


def get_config(cf: str) -> AdminConfigDict:
    if os.path.exists(cf):
        if not os.path.isfile(cf):
            raise FileNotFoundError(f'{cf} has been exist but not a file.')
        with open(cf, 'r', encoding='utf-8') as f:
            # HACK: config file may be corrupted.
            # add hash in config file? such as packages.json in node.
            return json.load(f)
    with open(cf, 'w', encoding='utf-8') as f:
        d = AdminConfigDict(users={})
        json.dump(d, f)
        return d

# region account


@routes.post('/admin/login')
async def login(request: Request):
    data = await request.post()
    username = data.get('username')
    password = data.get('password')
    config: AdminConfigDict = get_config()
    user: dict = config.get('users')
    if not user or len(user) == 0:
        return wrap_response(**ErrCode.NOT_INIT)
    cpwd = user.get(username)
    if cpwd:
        is_success = bcrypt.checkpw(password.encode(), cpwd)
        if is_success:
            return wrap_response()
    return wrap_response(**ErrCode.PWD_ERR)


@routes.get('/admin/logout')
async def logout(request: Request):
    return wrap_response()
# endregion

# region cache


@routes.post('/admin/cache')
async def del_cache(_: Request):
    await CacheDB().refresh_areas()
    return wrap_response()


@routes.post('/admin/cache/areas')
async def refresh_cache_areas(_: Request):
    await CacheDB().refresh_areas()
    return wrap_response()


@routes.post('/admin/cache/provinces/{area}')
async def refresh_cache_provinces(request: Request):
    area = request.match_info.get('area')
    await CacheDB().refresh_provinces(area)
    return wrap_response()


@routes.post('/admin/cache/ports/{province}')
async def refresh_cache_ports(request: Request):
    province = request.match_info.get('province')
    await CacheDB().refresh_ports(province)
    return wrap_response()


@routes.post('/admin/cache/tides')
async def refresh_cache_tides(_: Request):
    CacheUtil().get_tide.cache_clear()
    return wrap_response
# endregion

# region crawler


def crawl_result_converter(results: Tuple[ExecState, Union[Optional[WithInfo], Exception]]):
    (ret, obj) = results
    if ret in [ExecState.CREATE, ExecState.UPDATE, ExecState.SUCCESS]:
        return (ret, obj.objectId)
    else:
        return (ret, obj.rid)


@routes.post('/admin/crawl/areas')
async def crawl_areas(request: Request):
    save = (await request.post()).get('save')
    if save:
        await crawl.crawl_areas()
    data = await CrawlerService().crawl_areas()


@routes.post('/admin/crawl/provinces/{area}')
async def crawl_provinces(request: Request):
    area = request.match_info.get('area')
    await CrawlerService().crawl_provinces(area)


@routes.post('/admin/crawl/ports/{province}')
async def crawl_ports(request: Request):
    province = request.match_info.get('province')
    await CrawlerService().crawl_ports(province)

# endregion
