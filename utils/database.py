#!/usr/bin/env python
# coding=utf-8

import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class DbContext(object):

    def __init__(self, engine, session):
        self.engine = engine
        self.session = session

Base = declarative_base()
_db_contexts = {}


def _create_context(dbconfig, isdefault=False):
    if dbconfig["engine"] == "sqlite":
        url = dbconfig["engine"] + ":///" + dbconfig["file"]
        key = dbconfig.get("name") or dbconfig["file"]
    else:
        driver = dbconfig.get("driver")
        if driver:
            engine_str = dbconfig["engine"] + "+" + dbconfig["driver"]
        else:
            engine_str = dbconfig["engine"]
        if dbconfig["port"]:
            url = engine_str + "://" + dbconfig["user"] + \
                ":" + dbconfig["password"] + "@" + dbconfig["host"] + \
                ":" + "%s" % dbconfig["port"] + "/" + dbconfig["database"]
        else:
            url = engine_str + "://" + dbconfig["user"] + \
                ":" + dbconfig["password"] + "@" + \
                dbconfig["host"] + "/" + dbconfig["database"]
        """
        if dbconfig["port"]:
            url = dbconfig["engine"] + "+" + dbconfig["driver"] + "://" + dbconfig["user"] + \
                ":" + dbconfig["password"] + "@" + dbconfig["host"] + \
                ":" + "%s" % dbconfig["port"] + "/" + dbconfig["database"]
        else:
            url = dbconfig["engine"] + "+" + dbconfig["driver"] + "://" + dbconfig["user"] + \
                ":" + dbconfig["password"] + "@" + \
                dbconfig["host"] + "/" + dbconfig["database"]
        """
        key = dbconfig.get("name") or dbconfig["database"]
    if key in _db_contexts:
        return
    logging.debug("[_create_context][url: %s]" % url)
    engine = create_engine(url, connect_args=dbconfig.get("connect_args", {}), pool_recycle=5)
    Session = sessionmaker(bind=engine)
    session = Session()
    db_context = DbContext(engine, session)
    _db_contexts[key] = db_context
    if isdefault:
        _db_contexts["default"] = db_context


def db_init(dbconfig):
    if _db_contexts:
        return
    if isinstance(dbconfig, list):
        dbconfigs = dbconfig
    else:
        dbconfigs = [dbconfig]
    first = True
    for dbconfig in dbconfigs:
        if first:
            _create_context(dbconfig, True)
            first = False
        else:
            _create_context(dbconfig)


def create_db():
    if not _db_contexts:
        return False
    Base.metadata.create_all(_db_contexts["default"].engine)
    return True


def get_dbsession(name="default"):
    return _db_contexts[name].session


def get_engine(name="default"):
    return _db_contexts[name].engine


def get_dbconnection(name="default"):
    return _db_contexts[name].engine.connect()


@contextmanager
def dbsession(name="default"):
    try:
        yield _db_contexts[name].session
    except RuntimeError:
        pass
    finally:
        pass
