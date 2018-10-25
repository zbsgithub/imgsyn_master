#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/12 17:13
# @Author  : Aries
# @Site    : 
# @File    : run_app.py
# @Software: PyCharm

'''
程序入口
'''

import json
import multiprocessing as mp
from functools import partial
import time
import paramiko as pmk
from rsync.rsync_slave import transition
import traceback

from log.log import log_init
from archive.archive_handle import execute_handle
'''
检查连接
'''


def check_ssh(host, user, port, passwd, dest_path):
    ssh_client = pmk.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(pmk.AutoAddPolicy())
    try:
        ssh_client.connect(host, username=user, port=port, timeout=10, password=passwd)
        # 是在远程的机器上(c1、c2)读的
        # ssh_client.exec_command('mkdir ' + os.path.join(dest_path, "2018-10-20"))
    except BaseException as e:
        print('failed to connect to host: %r: %r' % (host, e))
        return False
    else:
        print('连通了')
        return True


# 全局路径变量
local_base_path = '/data/snapshots_v1/'
remote_base_path = '/data/snapshots/'

if __name__ == '__main__':
    print('--------------begin perfom application---------------------- ')

    file = open('collect_ip.json', 'r', encoding='utf-8')
    ci_array = json.load(file)

    # 读取日志文件
    file_log = open('loggin_conf.json', 'r', encoding='utf-8')
    ci_array_log = json.load(file_log)
    log_init(ci_array_log['logging'])

    pool = mp.Pool(processes=5)  # 进程池
    p_work = partial(transition, remote_base_path, local_base_path)  # 执行函数及传入相关参数

    for item in ci_array:
        print(item.get("mac_name"))
        '''
        多进程执行同步任务
        '''
        try:

            if not check_ssh(host=item.get("ip"), user=item.get("account"), port=item.get("port"),
                             passwd=item.get("pwd"), dest_path="/data/snapshots/"):
                print
                'SSH connect faild!'
                exit(-1)
            # pool.map(p_work, datetime.datetime.now().strftime('%Y-%m-%d'))

            # t = pmk.Transport((item.get("ip"), item.get("port")))
            # t.connect(username=item.get("account"), password=item.get("pwd"))
            # sftp = pmk.SFTPClient.from_transport(t)
            # 方法一
            # p_work = partial(transition, remote_base_path, local_base_path, sftp, t)  # 执行函数及传入相关参数
            pool.map(p_work, (item, ))

            # 方法二
            # transition(remote_base_path, local_base_path, sftp, t)

            time.sleep(10)
        except:
            print("unknow exception: ", traceback.format_exc())
    pool.terminate()
    pool.join()

    file.close()

    execute_handle('excute')
    print('---------------end  perform application---------------------')
