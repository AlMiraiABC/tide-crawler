"""Models for location"""
from crawler.model.base import BaseModel


class PortInfo(BaseModel):
    """港口信息"""

    def __init__(self, area_id: str, port_id: str, latitude: float, longitude: float, name: str, raw: str = ''):
        """
        :param area_id: Location area id of port. Foreign key to :class:`AreaInfo`
        :param port_id: Id of port
        :param latitude: Coordx
        :param longitude: Coordy
        :param name: Name of port
        """
        self.id = port_id
        self.latitude = latitude
        self.longitude = longitude
        self.areaId = area_id
        self.name = name
        self.raw = raw


class AreaInfo(BaseModel):
    """地区信息"""

    def __init__(self, id: str, name: str, raw: str = '') -> None:
        self.id = id
        self.name = name
        self.raw = raw
