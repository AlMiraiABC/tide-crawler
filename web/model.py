from datetime import datetime
from typing import Callable, List, Tuple, TypedDict

from aiohttp import web
from aiohttp.web import Response
from storages.model import Area, Port, Province, Tide, TideItemDict, WithInfo


class BaseModel(TypedDict):
    id: str
    name: str


class AreaModel(BaseModel):
    pass


class ProvinceModel(BaseModel):
    pass


class PortModel(BaseModel):
    zone: str
    geopoint: Tuple[float, float]


class TideModel(TypedDict):
    date: datetime.date
    day: List[TideItemDict]
    limit: List[TideItemDict]
    datum: float


class BaseResponse(TypedDict):
    code: int
    msg: str
    err: str
    data: any


def wrap_response(data={}, code=0, msg='success', err='') -> Response:
    resp = BaseResponse(code=code, msg=msg, err=err, data=data)
    return web.json_response(resp)


def to_base_model(o: WithInfo) -> BaseModel:
    if not o:
        return None
    return BaseModel(id=o.objectId, name=o.name)


def to_area_model(o: Area) -> AreaModel:
    return to_base_model(o)


def to_province_model(o: Province) -> ProvinceModel:
    return to_base_model(o)


def to_port_model(o: Port) -> PortModel:
    if not o:
        return None
    m = to_base_model(o)
    m.update({'zone': o.zone, 'geopoint': o.geopoint})
    return m


def to_tide_model(o: Tide) -> TideModel:
    if not o:
        return None
    return TideModel(date=o.date, day=o.day, limit=o.limit, datum=o.datum)


def to_models(os: list, to: Callable[[WithInfo], BaseModel]):
    return [to(o) for o in os]
