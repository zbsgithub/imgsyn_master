#!/usr/bin/env python
# coding=utf-8

import os
import datetime
import logging


class FileGroup(object):
    def __init__(self, files, datetime_pos=-1, separator=",", datetime_format="%Y-%m-%d %H:%M:%S"):
        self._files = files
        self._datetime_pos = datetime_pos
        self._separator = separator
        self._datetime_format = datetime_format
        self._file_objects = []
        self._open_all()
        self._last_read_path = None

    def _open_all(self):
        for filename in self._files:
            try:
                fd = open(filename, "rb")
                item = {
                    "filepath": os.path.split(filename)[0],
                    "filename": filename,
                    "fd": fd,
                }
                record = self._get_record(fd)
                if not record:
                    fd.close()
                    continue
                item["line"] = record
                self._file_objects.append(item)
            except:
                logging.error("[FileGroup::_open_all][open %s fail]" % filename)
                continue

    def __iter__(self):
        return self

    def __next__(self):
        if not self._file_objects:
            raise StopIteration
        result = self._get_oldest_line()

        new_line = self._get_record(self._file_objects[0]["fd"])
        if not new_line:
            self._file_objects[0]["fd"].close()
            self._file_objects.remove(self._file_objects[0])
        else:
            self._file_objects[0]["line"] = new_line
        """
        while self._file_objects:
            new_line = self._get_record(self._file_objects[0]["fd"])
            if not new_line:
                self._file_objects.remove(self._file_objects[0])
                continue
            self._file_objects[0]["line"] = new_line
            break
        """
        return result

    def last_readed_path(self):
        return self._last_read_path

    def _get_oldest_line(self):
        self._file_objects.sort(lambda x, y: cmp(x["line"][self._datetime_pos], y["line"][self._datetime_pos]))
        self._last_read_path = self._file_objects[0]["filepath"]
        return self._file_objects[0]["line"]

    def _get_record(self, fd):
        while True:
            try:
                line = fd.readline()
                if not line:
                    return None
                line = line.strip()
                line = line.split(self._separator)
                line[self._datetime_pos] = datetime.datetime.strptime(line[self._datetime_pos], self._datetime_format)
                return line
            except:
                continue
        return None
