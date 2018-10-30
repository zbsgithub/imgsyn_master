# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from utils.iplocation import get_location
from utils import locationcode


def address_gz_code(city, ip=None, ip_position=False):
    province_code, city_code = locationcode.code(city)

    if not province_code and ip_position or not city_code and ip_position:
        ip_loc = get_location(ip)
        province_code = ip_loc.province
        city_code = ip_loc.city

        if province_code == '900000' or city_code == '900000':
            province_code = 'all'
            city_code = 'all'

    province_code = province_code if province_code else "all"
    city_code = city_code if city_code else "all"

    return province_code, city_code



