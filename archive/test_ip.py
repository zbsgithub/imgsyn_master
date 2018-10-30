#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 15:44
# @Author  : Aries
# @Site    : 
# @File    : test_ip.py
# @Software: PyCharm

from utils.iplocation import get_locale_number,init
import logging

if __name__ == '__main__':
    logging.info("-------------------begin-----------------")
    init("../meta/qqwry.dat")
    ip_gps = get_locale_number("121.69.85.74")
    print(ip_gps)
    logging.info("-------------------end-----------------")

