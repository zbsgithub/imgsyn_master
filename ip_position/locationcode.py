# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from singleton import Singleton
from threading import Lock
# from apscheduler.schedulers.background import BackgroundScheduler

_code_lib = None


class BaseCronScheduler(object):

    def __init__(self, scheduler):
        self._scheduler = scheduler

    def start(self):
        self._scheduler.start()

    def stop(self):
        self._scheduler.shutdown()

    def install(self, job, hour):
        self._scheduler.add_job(job, "cron", hour=hour)


# class _LocationCode(BaseCronScheduler):
class _LocationCode(object):
    __metaclass__ = Singleton

    def __init__(self, code_file, reload_hour=2):
        # super(_LocationCode, self).__init__(BackgroundScheduler())
        self._code_file = code_file
        self._code_lib = dict()
        self._lock = Lock()
        self._reload_hour = reload_hour
        self._load_lib()
        # self._run_cron_task()

    def _run_cron_task(self):
        # self.install(self._load_lib, hour=self._reload_hour)
        # self.start()
        pass

    def _load_lib(self):
        with open(self._code_file, 'r') as f:
            for line in f:
                gz_province_code, _, city, gz_city_code, _ = line.split(',')
                self._code_lib[city] = {
                    'province': gz_province_code,
                    'city': gz_city_code,
                }

    def code(self, loc):
        try:
            info = self._code_lib[loc]
            return info['province'], info['city']
        except KeyError:
            return None, None

    def __del__(self):
        # self.stop()
        pass


def load_location_code(code_file):
    global _code_lib
    _code_lib = _LocationCode(code_file=code_file)


def code(location):
    return _code_lib.code(location)
