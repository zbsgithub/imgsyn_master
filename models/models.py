#!/usr/bin/env python
# coding=utf-8

from utils.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER


class QQwryLocale(Base):
    __tablename__ = "sys_locale_qqwry"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(30))
    locale_id = Column("locale_id", Integer)
    number = Column("number", Integer)
    locale_name = Column("locale_name", String(50))
    is_auto_sync = Column("is_auto_sync", Boolean)
    contributor_id = Column("contributor_id", Integer)
    checker_id = Column("checker_id", Integer)
    latest_update = Column("latest_update", DateTime)
    checker_id = Column("checker_id", Integer)
    latest_update = Column("latest_update", Integer)
    create_date = Column("create_date", Integer)


"""
class TvException(Base):
    __tablename__ = "tv_exceptions"

    id = Column("id", Integer, primary_key=True)
    gzid = Column("gzid", String(64))
    mac = Column("mac", String(32))
    device_id = Column("device_id", String(64))
    device_num = Column("device_num", String(64))
    oem_name = Column("oem_name", String(64))
    device_name = Column("device_name", String(64))
    device_model = Column("device_model", String(64))
    version_name = Column("version_name", String(64))
    exception = Column("exception", Text)
    exception_name = Column("exception_name", String(64))
    create_date = Column("create_date", DateTime)
"""


class TvClientException(Base):
    __tablename__ = "tv_client_exception"

    id = Column("id", Integer, primary_key=True)
    gzid = Column("gzid", String(64))
    mac = Column("mac", String(32))
    device_id = Column("device_id", String(64))
    # device_num = Column("device_num", String(64))
    oem_name = Column("oem_name", String(64))
    device_name = Column("device_name", String(64))
    device_model = Column("device_model", String(64))
    version = Column("version", String(64))
    name = Column("name", String(64))
    detail_id = Column("detail_id", UNIQUEIDENTIFIER)
    create_date = Column("create_date", DateTime)
    router_ip = Column("router_ip", String(64))


class TvClientExceptionDetail(Base):
    __tablename__ = "tv_client_exception_detail"

    id = Column("id", UNIQUEIDENTIFIER, primary_key=True)
    exception = Column("exception", Text)


class GzCryptKey(Base):
    __tablename__ = "gz_crypt_keys"

    id = Column("id", Integer, primary_key=True)
    version = Column("version", String(64))
    key = Column("key", String(64))
    index = Column("index", Integer)


class SysSubOem(Base):
    __tablename__ = "sys_sub_oem"

    id = Column("id", Integer, primary_key=True)
    oem_name = Column("oem_name", String(64))
    sub_oem = Column("sub_oem", String(64))
    device_name = Column("device_name", String(64))


class SysOemBrand(Base):
    __tablename__ = "sys_oem_brand"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(64))
    is_checked = Column("is_checked", Boolean)


"""
class DeviceInfo(Base):
    __tablename__ = "deviceinfos"

    id = Column("id", Integer, primary_key=True)
    oem_name = Column("oem_name", String(64))
    device_id = Column("device_id", String(64))
    device_name = Column("device_name", String(64))
    device_model = Column("device_model", String(64))
    deveice_num = Column("device_num", String(64))
    version_name = Column("version_name", String(64))
    remote_ip = Column("remote_ip", String(32))
    update_time = Column("update_time", DateTime)


class DeviceOnlineStatistic(Base):
    __tablename__ = "device_online_statistics"

    id = Column("id", Integer, primary_key=True)
    oem_name = Column("oem_name", String(64))
    device_name = Column("device_name", String(64))
    device_model = Column("device_model", String(64))
    version_name = Column("version_name", String(64))
    online_count = Column("online_count", Integer)
    datetime = Column("datetime", DateTime)
"""

if __name__ == "__main__":
    from utils.database import get_db_session

    for row in get_db_session().query(QQwryLocale).all():
        print(row.id, row.name)

