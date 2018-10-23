#!/usr/bin/env python
# coding=utf-8

import logging

from models.models import QQwryLocale
# from utils.database import get_db_session
from utils.database import dbsession
from utils.qqwry import IPInfo
from utils.lru import LruCache

_ip_info = None
_locale = None
_cache_dir = LruCache(500000)


class _Locale(object):
    def __init__(self, dbname):
        self._dbname = dbname
        self._locale_dict = {}
        self._load_data()

    def get_locale_number(self, address):
        return self._locale_dict.get(address)

    def _load_data(self):
        """
        for row in get_db_session().query(QQwryLocale).all():
        for row in get_db_session().query(QQwryLocale).all():
            self._locale_dict[row.name] = row.number
        logging.info("[_Locale::_load_data][qqwry locale count: %s]" % len (self._locale_dict))
        """
        """
        """
        with dbsession(self._dbname) as session:
            for row in session.query(QQwryLocale).all():
                self._locale_dict[row.name] = row.number
        logging.info("[_Locale::_load_data][qqwry locale count: %s]" % len(self._locale_dict))


def init(qqwry_file, dbname="default"):
    global _ip_info
    global _locale
    if _ip_info:
        return
    _ip_info = IPInfo(qqwry_file)
    _locale = _Locale(dbname)


def get_locale_number(ipstr):
    global _ip_info
    global _locale
    if not ipstr or not _ip_info:
        return None
    """
    number = _cache_dir.get(ipstr)
    if number:
        return number
    """
    address = _ip_info.get_ip_addr(ipstr)

    # print address[0], address[1]
    number = _locale.get_locale_number(address[0])
    """
    if number:
        # cache_dir[ipstr] = number
        _cache_dir.set(ipstr, number)
    """
    return number
