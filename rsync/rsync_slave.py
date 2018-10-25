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
同步文件
'''

def sync_file(file_absoult_array, sftp, local_base_path, remote_base_path, t):

    # 下载文件到本地
    for file_sub in file_absoult_array:
        local_path = local_base_path + os.sep + file_sub

        if not os.path.exists(local_base_path + file_sub.split("/")[0]+"/"+file_sub.split("/")[1]+"/"):
            os.makedirs(local_base_path + file_sub.split("/")[0]+"/"+file_sub.split("/")[1]+"/")
        try:
            # 判断是否有这个文件
            sftp.file(remote_base_path + file_sub)
            # 使用get()方法拉去文件
            sftp.get(remote_base_path + file_sub, local_path)
        except IOError as e:
            logging.info(remote_base_path +file_sub+ " remote file not exist!")
            sys.exit(1)
        finally:
            # t.close()
            print('transport')
    t.close()
    logging.info("----------------文件同步到本地结束---------------------")
'''
过渡方法
'''
def transition(remote_base_path, local_base_path, args):
    t = pmk.Transport((args["ip"], args["port"]))
    t.connect(username=args["account"], password=args["pwd"])
    sftp = pmk.SFTPClient.from_transport(t)

    yesterday_day = datetime.datetime.now().date() - datetime.timedelta(days=1)
    current_date = yesterday_day.strftime('%Y-%m-%d')  # 当前日期
    files = sftp.listdir(remote_base_path + current_date + "/")  # 这里需要注意，列出远程文件必须使用sftp，而不能用os
    file_list_array = []

    # 列出当天采集节点下的mac文件夹
    for f in files:
        file_list_array.append(f)

    # mac 下的文件元信息及图片路径
    file_list_array_second = []

    fils_final = sftp.listdir(remote_base_path + current_date + "/"+file_list_array[0])
    for item in fils_final:
        if item == "snapshots":
            pass
        else:
            file_list_array_second.append(current_date +"/" + file_list_array[0]+ "/"+item)

    sync_file(file_list_array_second, sftp, local_base_path, remote_base_path, t)
