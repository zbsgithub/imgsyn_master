# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from ip_position.iplocation import init,get_location

ip_cfg = {
    "ip_pos_on": 1,
    "ip_file": "geoip.dat",
    "name_file": "names",
    "update_hour": 2
}

init(ip_file=ip_cfg['ip_file'], address_file=ip_cfg["name_file"])

'''
According ip return city gps info
'''
def get_ip_position(ip_address):
    ip_loc = get_location(ip_address)
    # province_code = ip_loc.province
    city_code = int(float(ip_loc.city))
    return city_code

if __name__ == "__main__":
    ip_loc = get_location(sys.argv[1])
    province_code = ip_loc.province
    city_code = ip_loc.city
    print(province_code, city_code)


