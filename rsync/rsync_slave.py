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

'''
同步文件
'''


# local_base_path 本地基础路径 /data/snapshots_v1/
# remote_base_path 远程基础路径 /data/snapshots/
def sync_file(file_absoult_array, sftp, local_base_path, remote_base_path, t):
    # 从远程下载文件到本地 scp root@47.94.35.234:/data/snapshots/2018-10-14/00163E001D8F/0-metainfo.txt /data/snapshots_v1/
    # remotepath = '/data/snapshots/2018-10-14/00163E001D8F/0-metainfo.txt'
    # localpath = local_base_path + os.sep + '0-metainfo.txt'

    # 下载文件到本地
    for file_sub in file_absoult_array:
        local_path = local_base_path + os.sep + file_sub
        # print(remote_base_path + file_sub)
        # print(local_path)
        # sftp.get(remote_base_path + file_sub, local_path)

        # 如果当前程序所在服务器没目标目录则创建
        if not os.path.exists(local_base_path + file_sub.split("/")[0]+"/"+file_sub.split("/")[1]+"/"):
            os.makedirs(local_base_path + file_sub.split("/")[0]+"/"+file_sub.split("/")[1]+"/")
        #以下为正确代码
        try:
            print(remote_base_path + file_sub)
            # 判断远程服务器是否有这个文件
            sftp.file(remote_base_path + file_sub)
            # 使用get()方法从远程服务器拉去文件
            sftp.get(remote_base_path + file_sub, local_path)
        except IOError as e:
            print(remote_base_path +file_sub+ " remote file not exist!")
            sys.exit(1)
        finally:
            # t.close()
            print('transport')
    t.close()
    print('----------------文件同步到本地结束---------------------')
'''
过渡方法
'''


# remote_base_path "/data/snapshots/"
# local_base_path 本地存放路径 "/data/snapshots_v1/"
def transition(remote_base_path, local_base_path, args):
    t = pmk.Transport((args["ip"], args["port"]))
    t.connect(username=args["account"], password=args["pwd"])
    sftp = pmk.SFTPClient.from_transport(t)

    yesterday_day = datetime.datetime.now().date() - datetime.timedelta(days=1)
    current_date = yesterday_day.strftime('%Y-%m-%d')  # 当前日期
    # current_date = '2018-10-14'
    # 测试代码 路径： /data/snapshots/2018-10-14/00163E001D8F/
    files = sftp.listdir(remote_base_path + current_date + "/")  # 这里需要注意，列出远程文件必须使用sftp，而不能用os
    file_list_array = []

    # 列出当天采集节点下的mac文件夹
    for f in files:
        print(f)
        file_list_array.append(f)

    print(file_list_array)
    # mac 下的文件元信息及图片路径
    file_list_array_second = []

    fils_final = sftp.listdir(remote_base_path + current_date + "/"+file_list_array[0])
    for item in fils_final:
        if item == "snapshots":
            pass
        else:
            file_list_array_second.append(current_date +"/" + file_list_array[0]+ "/"+item)
    print(file_list_array_second)
    # print('最终要的路径：' + file_list_array_second)  # 所有要同步的文件的绝对路径

    sync_file(file_list_array_second, sftp, local_base_path, remote_base_path, t)

    print('--------------------------程序执行完成------------------------------')
