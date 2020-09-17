import urllib.parse
from typing import List

import requests

from config import HEADERS
from util.time import Timestamp

"""
获得所有港口及其对应的代码
"""


class Selector:

    @staticmethod
    def get_countries(continent_name: str) -> List[str]:
        """
        根据洲名查询国家

        https://www.cnss.com.cn/tide/find.jspx?state=%E4%BA%9A%E6%B4%B2

        :param continent_name: 洲名，例如亚洲
        :return: 国家名列表
        """
        params = {
            'state': continent_name
        }
        params_url = urllib.parse.urlencode(params)
        base_url = "https://www.cnss.com.cn/tide/find.jspx?"
        full_url = base_url + params_url
        response = requests.get(url=full_url, headers=HEADERS)
        return response.json()

    @staticmethod
    def get_china_provinces() -> List[str]:
        """
        根据洲名和国家名查询所对应的省份

        find接口当country为中国时返回省份，其他国家时返回港口
        https://www.cnss.com.cn/tide/find.jspx?country=%E4%B8%AD%E5%9B%BD&state=%E4%BA%9A%E6%B4%B2

        :return: 省名列表
        """
        params = {
            'country': '中国',
            'state': '亚洲'
        }
        params_url = urllib.parse.urlencode(params)
        base_url = "https://www.cnss.com.cn/tide/find.jspx?"
        full_url = base_url + params_url
        response = requests.get(url=full_url, headers=HEADERS)
        return response.json()

    @staticmethod
    def get_other_countries_ports(country_name: str) -> List[str]:
        """
        根据国家名（不包括中国）查询该国的港口名

        find接口当country为中国时返回省份，其他国家时返回港口
        https://www.cnss.com.cn/tide/find.jspx?country=%E6%96%B0%E5%8A%A0%E5%9D%A1

        :param country_name: 国家名
        :return: 港口名列表
        """
        params = {
            'country': country_name
        }
        params_url = urllib.parse.urlencode(params)
        base_url = "https://www.cnss.com.cn/tide/find.jspx?"
        full_url = base_url + params_url
        response = requests.get(url=full_url, headers=HEADERS)
        return response.json()

    @staticmethod
    def get_china_province_ports(province_name: str) -> List[str]:
        """
        根据中国的省名查询所对应的港口名

        先获取中国的省份才能获取到各省的港口
        https://www.cnss.com.cn/tide/find.jspx?province=%E8%BE%BD%E5%AE%81

        :param province_name: 中国的省名
        :return: 港口名列表
        """
        params = {
            'province': province_name
        }
        params_url = urllib.parse.urlencode(params)
        base_url = "https://www.cnss.com.cn/tide/find.jspx?"
        full_url = base_url + params_url
        response = requests.get(url=full_url, headers=HEADERS)
        return response.json()

    @staticmethod
    def get_port_info(seaport_name: str):
        """
        根据港口名确获得该港口的信息

        https://www.cnss.com.cn/u/cms/www/portJson/%E5%8D%97%E6%B5%A6.json?v=1586672361881

        :param seaport_name: 港口名
        :return: 该港口的ID
        """
        params = {
            'v': Timestamp.timestamp_to_spec()
        }
        quote = urllib.parse.quote(seaport_name)
        base_url = "https://www.cnss.com.cn/u/cms/www/portJson/" + quote + ".json?"
        response = requests.get(url=base_url, headers=HEADERS, params=params)
        data: dict = response.json()
        return PortInfo(
            int(data.get('portId')),
            float(data.get('latitudeFv')),
            float(data.get('longitudeFv')),
            float(data.get('tideDatum')),
            data.get('timeZone'))


class PortInfo:
    def __init__(self, seaport_id: int, latitude: float, longitude: float, datum: float, zone: str):
        self.portId = seaport_id
        self.latitude = latitude
        self.longitude = longitude
        self.datum = datum
        self.zone = zone

#
# if __name__ == '__main__':
#     port_list = []
#     # '亚洲','北美洲', '南美洲', '大洋洲', '南极洲', '非洲', '欧洲'
#     # 洲名
#     continents = ['亚洲', '北美洲', '南美洲', '大洋洲', '南极洲', '非洲', '欧洲']
#     for continent in continents:
#         countries = Selector.get_countries(continent)
#         for country in countries:  # 遍历国家
#             if country == "中国":
#                 print("********" + country + "***********")
#                 provinces = Selector.get_china_provinces()
#                 for province in provinces:
#                     print("%%%%%%%%%%%%%%" + province + "%%%%%%%%%%%%%%%%")
#                     ports = get_china_province_ports(province)
#                     for port_name in ports:
#                         port = {}
#                         port_id = get_port_id(port_name)
#                         port['name'] = port_name
#                         port['id'] = port_id
#                         port_list.append(port)
#             else:
#                 print("********" + country + "***********")
#                 ports = get_other_countries_ports(country)
#                 for port_name in ports:
#                     port = {}
#                     port_id = get_port_id(port_name)
#                     port['name'] = port_name
#                     port['id'] = port_id
#                     port_list.append(port)
#     print(port_list)
