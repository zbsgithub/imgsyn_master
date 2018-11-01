#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 15:28
# @Author  : Aries
# @Site    : 
# @File    : clear_task.py
# @Software: PyCharm

import shutil
import logging
import os
import datetime
from datetime import timedelta

'''
all clear jobs
'''
def clear_jobs(ci_array_log):

    recursive_delete_tmp()
    logging.info("clear temp tmp/ file success ")
    clear_rsync_snapshot_archives(ci_array_log)
    logging.info("clear snapshot_archives success ")
    clear_rsync_snapshot(ci_array_log)
    logging.info("clear snapshot  success ")
'''
clear tmp dirs log file 
'''
def recursive_delete_tmp():
    shutil.rmtree("/tmp/pack_snapshot_v1/")
    logging.info("recursive delete tmp below pack_snapshot_v1 over")


'''
clear snapshot_archives file
Only for nearly three days
'''
def clear_rsync_snapshot_archives(ci_array_log):
    local_base_path = ci_array_log["dst_path"]
    near_three_days = []  # near three days array
    for x in range(3):
        current_day = (datetime.datetime.now() - datetime.timedelta(days=x + 1)).strftime('%Y-%m-%d')
        near_three_days.append(current_day)
    two_date_array = []  # second dirs arrays
    for dir in os.listdir(local_base_path):
        os.path.join(local_base_path, dir)
        two_date_array += [os.path.join(local_base_path, dir) + os.sep + x for x in
                           os.listdir(os.path.join(local_base_path, dir))]
    print(two_date_array)
    for item in two_date_array:
        sub_day = item[-10:]
        if sub_day in near_three_days:
            pass
        else:
            # shutil.rmtree(os.path.join(item+os.sep))# recursion delete near three day beside dirs
            logging.info('three day beside dirs : %s ' % item)

'''
clear snapshot_archives file
Only for nearly three days
'''
def clear_rsync_snapshot(ci_array_log):
    local_base_path = ci_array_log["source_path"]
    near_three_days = []  # near three days array
    for x in range(3):
        current_day = (datetime.datetime.now() - datetime.timedelta(days=x + 1)).strftime('%Y-%m-%d')
        near_three_days.append(current_day)

    two_date_array = []  # second dirs arrays
    for dir in os.listdir(local_base_path):

        two_date_array.append(os.path.join(local_base_path, dir))

    print(two_date_array)
    for item in two_date_array:
        sub_day = item[-10:]
        if sub_day in near_three_days:
            pass
        else:
            # shutil.rmtree(os.path.join(item+os.sep))# recursion delete near three day beside dirs
            logging.info('three day beside dirs : %s ' % item)





if __name__ == '__main__':
    pass

