from typing import Awaitable, Callable, Dict, List, Tuple, Type

from aiohttp import web
from aiohttp.web import Request, Response

HandleType = Callable[[Request], Awaitable[ Response]]


_http_handler: Dict[int, HandleType] = {}
_exception_handler: List[Tuple[Type[Exception], HandleType]] = []


def http(status: int):
    def wrap(f):
        _http_handler[status, f]
        return f
    return wrap


def ex(ex_type: Type[Exception]):
    def wrap(f):
        _exception_handler.append((ex_type, f))
        return f
    return wrap


@web.middleware
async def error_middleware(request: Request, handler: HandleType):
    try:
        response = await handler(request)
        return response
    except web.HTTPException as ex:
        if ex.status in _http_handler:
            return await _http_handler[ex.status](request)
        raise
    except Exception as err:
        for t, h in _exception_handler:
            if isinstance(err, t):
                return await h(request)
        return web.Response(status=500, reason=str(err))
