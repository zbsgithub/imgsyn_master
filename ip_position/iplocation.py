# -*- coding: utf-8 -*-
import socket
from struct import pack, unpack


ip_table = []
address_dict = {}
default_area = "900000"
default_address = u"其他"


class _Location(object):
    def __init__(self, area):
        self.area = area
        self._area_value = int(area)

    @property
    def province(self):
        return "%s" % (self._area_value / 100 * 100)

    @property
    def city(self):
        return "%s" % (self._area_value / 10000 * 10000)

    @property
    def province_name(self):
        province = self.province
        return address_dict.get(province, default_address)

    @property
    def city_name(self):
        city = self.city
        return address_dict.get(city, default_address)


def init(ip_file, address_file):
    with open(ip_file) as fd:
        for line in fd:
            line = line.strip()
            items = line.split(",")
            start_ip = int(items[0])
            end_ip = int(items[1])
            area = items[2]
            ip_table.append((start_ip, end_ip, area))

    with open(address_file) as fd:
        for line in fd:
            line = line.strip()
            items = line.split("\t")
            area = items[0]
            address = items[1]
            address_dict[area] = address
            address_dict[default_area] = default_address


def get_location(ipstr):
    try:
        ip = unpack('!I', socket.inet_aton(ipstr))[0]
    except:
        return _Location(default_area)
    low = 0
    high = len(ip_table) - 1
    while True:
        if low > high:
            break
        middle = (low + high) / 2
        item = ip_table[int(middle)]
        if ip > item[1]:
            low = middle + 1
        elif ip < item[0]:
            high = middle - 1
        else:
            return _Location(item[2])
    return _Location(default_area)


