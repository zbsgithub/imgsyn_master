#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/17 18:09
# @Author  : Aries
# @Site    :
# @File    : __init__.py.py
# @Software: PyCharm
'''
主要功能：
    图片分类归档处理
'''

import datetime
import os
import logging
import csv
import shutil
import traceback
import random
import json

from mongoengine import Document, StringField, DateTimeField, IntField

from utils.net import get_mac_address
from utils.file_group import FileGroup
from mongo.conn_handle import conn

from ip_position.main import get_ip_position

class SnapshotPackDistribution(Document):
    meta = {"collection": "snapshot_pack_distributions"}
    did = StringField(max_length=64)
    mac = StringField(max_length=64)
    create_time = DateTimeField()
    update_time = DateTimeField()


class SnapshotFile(object):
    def __init__(self, abs_file_name, meta):
        self.abs_file_name = abs_file_name
        self.meta = meta


class ArchiveTable(object):

    def __init__(self):
        self._archive_dict = {}
        self._archive_list = []
        self._current_handle_index = 0

    def add(self, machine_id, path_id, snapshot_file):
        key = (machine_id, path_id)
        path_obj = self._archive_dict.get(key)
        if not path_obj:
            path_obj = []
            self._archive_dict[key] = path_obj
            self._archive_list.append((machine_id, path_id, path_obj))
        path_obj.append(snapshot_file)

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_handle_index >= len(self._archive_list):
            raise StopIteration
        path_obj = self._archive_list[self._current_handle_index]
        self._current_handle_index += 1
        return path_obj

    def __len__(self):
        return len(self._archive_list)

    def clear(self):
        self._archive_dict.clear()
        del self._archive_list[:]
        self._current_handle_index = 0


class SnapshotActiveDeviceStatistic(Document):
    meta = {"collection": "snapshot_active_device_statistics"}
    datetime = DateTimeField()
    count = IntField()


class ArchiveHandler(object):
    def __init__(self, source_path, snapshot_subdir, dst_path, pack_machines, filename_suffix):
        self._source_path = source_path
        self._snapshot_subdir = snapshot_subdir
        self._dst_path = dst_path
        self._pack_machines = pack_machines
        self._filename_suffix = filename_suffix

        self._partitions = {}
        self._archive_table = ArchiveTable()

        self._target_day = datetime.datetime.now().date() - datetime.timedelta(days=1)
        self._target_time = datetime.datetime(
            self._target_day.year,
            self._target_day.month,
            self._target_day.day,
            0,
            0,
            0
        )
        self._target_day_str = self._target_day.strftime("%Y-%m-%d")

        self._target_paths = {}
        self._metainfo_files = []
        self._tmp_path = "/tmp/pack_snapshot_v1/"
        self._handled_count = 0

    def run(self):
        self.init()
        self.preprocess()
        self.archive()

    def init(self):
        for pack_machine in self._pack_machines:

            # target_path 格式：/data/snapshot_archives/00163E0031C6/2017-07-24
            target_path = os.path.join(self._dst_path, pack_machine, self._target_day_str)
            if not os.path.exists(target_path):
                try:
                    os.makedirs(target_path)
                except:
                    pass

            archive_metafile = os.path.join(target_path, "metafile.txt")
            target = {
                "machine_id": pack_machine,
                "target_path": target_path,
                "archive_metafile": archive_metafile,
            }
            self._target_paths[pack_machine] = target

        self._metainfo_files = self._get_all_metainfo_files()
        logging.debug("[ArchiveHandler::init][target_paths: %s]" % self._target_paths)

    def preprocess(self):
        total_line_count = -1
        piece_size = 1000

        for filename in self._metainfo_files:
            total_line_count += self.get_file_line_count(filename)

        piece_count = int(total_line_count / piece_size)
        if piece_count == 0:
            piece_count = 1

        logging.debug("[ArchiveHandler::preprocess][total_count: %s][piece_count: %s]" %
                     (total_line_count, piece_count))

        file_group = FileGroup(self._metainfo_files, datetime_pos=-3)

        try:
            shutil.rmtree(self._tmp_path)
        except:
            pass

        fds = {}
        try:
            os.mkdir(self._tmp_path)
        except:
            pass

        for index in range(0, piece_count):  # python3 取消了xrange

            abs_filename = os.path.join(self._tmp_path, "%s" % index)
            fds[index] = open(abs_filename, "wb")
        for line in file_group:
            try:
                width, height, timestamp, device_model, device_id, ip_address, \
                gzid, oem_name, device_num, device_name, fid, category, create_datetime, save_path, uid = line
            except:
                logging.info("[ArchiveHandler::preprocess][parse line fail][exception: %s][line: %s][len: %d]" %
                             (traceback.format_exc(), line, len(line)))
                continue

            piece_index = sum(map(ord, device_id)) % piece_count
            fd = fds.get(piece_index)
            try:
                line[12] = line[12].strftime("%Y-%m-%d %H:%M:%S")
            except:
                continue
            snapshot_abs_filename = os.path.join(file_group.last_readed_path(),
                                                 self._snapshot_subdir, "%s.jpg" % uid)
            line.append(snapshot_abs_filename)
            try:
                line = ",".join(line) + os.linesep
            except:
                continue
            fd.write(bytes(line, encoding='utf-8'))
        for index, fd in fds.items():
            fd.close()

    @classmethod
    def get_file_line_count(cls, filenmae):
        count = -1
        try:
            with open(filenmae, "rU") as fd:
                for count, line in enumerate(fd):
                    pass
            count += 1
        except:
            return 0
        return count

    def archive(self):
        try:
            filenames = os.listdir(self._tmp_path)
        except:
            return
        for filename in filenames:
            abs_filename = os.path.join(self._tmp_path, filename)
            if not os.path.isfile(abs_filename):
                continue
            self._archive(abs_filename)
            self._compress()

    def _archive(self, filename):
        logging.info("[ArchiveHandler::_archive][filename: %s]" % filename)
        self._archive_table.clear()
        try:
            fd = open(filename, "rb")
        except:
            return
        for line in fd:
            # print(line)
            line = str(line, encoding="utf-8")
            line = line.strip()
            self._handled_count += 1
            if self._handled_count % 5000 == 0:
                logging.debug("[ArchiveHandler::archive][handled_count: %s]" % self._handled_count)
            try:
                width, height, timestamp, device_model, device_id, \
                ip_address, gzid, oem_name, device_num, device_name, fid, category, \
                create_datetime, save_path, uid, snapshot_abs_filename = line.split(",")

                timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                create_datetime = datetime.datetime.strptime(create_datetime, "%Y-%m-%d %H:%M:%S")
                create_datetime = create_datetime.strftime("%Y-%m-%dT%H:%M:%S")
            except:
                logging.info("[ArchiveHandler::archive][parse line fail][exception: %s][line: %s]" %
                             (traceback.format_exc(), line))
                continue
            # locale_number = iplocation.get_locale_number(ip_address)
            locale_number = get_ip_position(ip_address)
            pack_machine = self._choose_pack_machine(device_id)
            sub_path = "%s_%s_%s_%s" % (gzid, locale_number, device_id, self._target_day_str)
            meta = [
                uid,
                width,
                height,
                timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
                device_model,
                gzid,
                ip_address,
                create_datetime,
                oem_name,
                device_num,
                device_name,
                fid,
                category,
                save_path
            ]
            snapshot_file = SnapshotFile(snapshot_abs_filename, meta)
            self._archive_table.add(pack_machine, sub_path, snapshot_file)
        fd.close()
        logging.debug("[ArchiveHandler::_archive][handled_count: %s]" % self._handled_count)
        logging.debug("[ArchiveHandler::_archive][over...]")

    def _compress(self):
        logging.debug("[ArchiveHandler::_compress][archives count: %s]" % len(self._archive_table))
        compress_count = 0

        for path_obj in self._archive_table:
            compress_count += 1
            if compress_count % 5000 == 0:
                logging.info("[ArchiveHandler::_compress][compress_count: %s]" % compress_count)
            # mac地址 38ed6927-c41b-48ed-be6e-11f50b29dc8a_None_fca38669e6c0_2018-10-15 snapshot_files
            machine_id, path_id, snapshot_files = path_obj


            # logging.debug("[ArchiveHandler::_compress][machine_id: %s][path_id: %s]" % (machine_id, path_id))
            try:
                target_path_obj = self._target_paths[machine_id]#mac example：00163E001D8F
            except:
                logging.error("[ArchiveHandler::_compress][get target path error][machine_id: %s]" % machine_id)
                raise
            target_path = target_path_obj["target_path"]
            archive_metafile = target_path_obj["archive_metafile"]
            archive_abs_path = os.path.join(target_path, path_id)

            if not os.path.exists(archive_abs_path):
                try:
                    os.makedirs(archive_abs_path)
                except:
                    logging.error("[ArchiveHandler::_compress][makedirs fail][dir: %s]" % archive_abs_path)
                    pass

            list_file_name = os.path.join(archive_abs_path, "list.csv")
            list_file_descriptor = None
            try:
                list_file_descriptor = open(list_file_name, "w")
                meta_writer = csv.writer(list_file_descriptor, dialect="excel-tab")  # set write mode
            except:
                if list_file_descriptor:
                    list_file_descriptor.close()
                logging.error('writer error ：%s' % traceback.format_exc())
                continue

            count = 1
            for snapshot_file in snapshot_files:
                meta = snapshot_file.meta
                try:
                    meta_writer.writerow(meta)
                except:
                    logging.error('write list.csv file error：%s' % traceback.format_exc())
                    continue
                count += 1
            list_file_descriptor.close()

            archive_meta_fileobj = None
            try:
                archive_meta_fileobj = open(archive_metafile, "a")
                archive_meta_fileobj.write(path_id+"\n")
            except:
                logging.error("[ArchiveHandler::_compress][write meta info fail][path_id: %s][exception: %s]" %
                              (path_id, traceback.format_exc()))
            finally:
                if not archive_meta_fileobj:
                    archive_meta_fileobj.close()

        logging.debug("[ArchiveHandler::_compress][compress_count: %s]" % compress_count)

    def _copyfile(self, src, dst, length=16 * 1024):
        with open(src, 'rb') as fsrc:
            with open(dst, 'wb') as fdst:
                while 1:
                    buf = fsrc.read(length)
                    if not buf:
                        break
                    fdst.write(buf)

    def _choose_pack_machine(self, device_id):
        partition = self._partitions.get(device_id)#according did obtain about partition mac
        if not partition:
            partition_obj = conn("query", {"did": device_id})  # curretn partition object
            now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if not partition_obj:  # if null the rand insert to database
                # random born mac
                file_log = open('loggin_conf.json', 'r', encoding='utf-8')
                ci_array_log = json.load(file_log)

                random_partition = random.choice(ci_array_log['pack_machines'])#random distribution mac
                insert_json_obj = {"did": device_id, "mac": random_partition,
                                   "create_time": now_str,
                                   "update_time": now_str}
                conn("insert", insert_json_obj)
                return random_partition
            else:  # if exist so directly take mac value

                update_json_obj = {"did": device_id,
                                   "update_time": now_str,
                                   "mac": partition_obj["mac"]}
                conn("update", update_json_obj)
                self._partitions[device_id] = partition_obj["mac"]
                return partition_obj["mac"]
        return partition

    def _close_all(self):
        for key, value in self._archives.iteritems():
            value["fileobj"].close()

    def _get_all_metainfo_files(self):
        files = []
        base_path = os.path.join(self._source_path, self._target_day_str)
        for path_name in os.listdir(base_path):
            if len(path_name) != len(get_mac_address()):
                continue
            full_path = os.path.join(base_path, path_name)
            for file_name in os.listdir(full_path):
                if file_name.endswith(self._filename_suffix):
                    files.append(os.path.join(full_path, file_name))
        return files
'''
call perform method
'''
def execute_handle(ci_array_log):
    logging.info("---begin call archive program -----")

    logging.info("[main][start...]")
    archive_handler = ArchiveHandler(
        ci_array_log["source_path"],
        ci_array_log["snapshot_subdir"],
        ci_array_log["dst_path"],
        ci_array_log["pack_machines"],
        ci_array_log["filename_suffix"]
    )
    try:
        archive_handler.run()
    except:
        logging.error("[main][handle fail][exceptions: %s]" % traceback.format_exc())
    logging.info("---end call archive program -----")