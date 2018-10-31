#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/12 10:58
# @Author  : Aries
# @Site    : 
# @File    : rsync_slave.py.py
# @Software: PyCharm

import datetime
import os
import sys
import paramiko as pmk
import logging
'''
synchronous file
'''

def sync_file(file_absoult_array, sftp, local_base_path, remote_base_path, t):

    # download file to local
    for file_sub in file_absoult_array:
        local_path = local_base_path + os.sep + file_sub

        if not os.path.exists(local_base_path + file_sub.split("/")[0]+"/"+file_sub.split("/")[1]+"/"):
            os.makedirs(local_base_path + file_sub.split("/")[0]+"/"+file_sub.split("/")[1]+"/")
        try:
            # check remote file exist
            sftp.file(remote_base_path + file_sub)
            # use get() method pull file
            sftp.get(remote_base_path + file_sub, local_path)
        except IOError as e:
            logging.info(remote_base_path +file_sub+ " remote file not exist!")
            sys.exit(1)
    t.close()
    logging.info("------file sync to local over-----")
'''
transition method
'''
def transition(remote_base_path, local_base_path, args):
    t = pmk.Transport((args["ip"], args["port"]))
    t.connect(username=args["account"], password=args["pwd"])
    sftp = pmk.SFTPClient.from_transport(t)

    yesterday_day = datetime.datetime.now().date() - datetime.timedelta(days=1)
    current_date = yesterday_day.strftime('%Y-%m-%d')  # current date
    files = sftp.listdir(remote_base_path + current_date + "/")  # this attention show remote file use sftp method,don't use os
    file_list_array = []

    # show current day collect node mac dirs
    for f in files:
        file_list_array.append(f)

    # mac below file meta and file path
    file_list_array_second = []

    fils_final = sftp.listdir(remote_base_path + current_date + "/"+file_list_array[0])
    for item in fils_final:
        if item == "snapshots":
            pass
        else:
            file_list_array_second.append(current_date +"/" + file_list_array[0]+ "/"+item)

    sync_file(file_list_array_second, sftp, local_base_path, remote_base_path, t)
