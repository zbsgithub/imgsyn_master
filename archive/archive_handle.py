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

import os
import datetime

import contextlib
from contextlib import contextmanager
import time
from archive.date_time_utils import *
'''
某个路径下所有的子文件列表(绝对路径)
'''


def show_all_son_file():
    # base_path="/data/snapshots_v1/"+datetime.datetime.now().strftime('%Y-%m-%d')
    base_path = "/data/snapshots_v1/2018-10-14"
    result = []  # 所有的文件

    for maindir, subdir, file_name_list in os.walk(base_path):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)  # 合并成一个完整路径
            result.append(apath)

    return result


@contextmanager
def multipart_open_file(files=None, mode='r'):
    if files is None:
        files = []
    try:  # 相当于__enter__
        fds = []
        for f in files:
            fds.append(open(f, mode))
        yield fds
    except ValueError as e:
        print(e)
    finally:  # 相当于__exit__
        for fd in fds:
            fd.close()


# def sort_date_list(date_list, date_format, DESC=False):
#     """
#     1. 对日期进行排序
#     2. 输入是列表类型。
#     3. 默认降序方式
#     """
#     res_list = sorted(date_list, key=lambda date: datetime.datetime.strptime(date, date_format), reverse=DESC)
#     return res_list


'''
运行方法
'''
if __name__ == '__main__':
    # print(show_all_son_file()) #所有文件集合(绝对路径)

    result_array = show_all_son_file()  # 获取返回文件列表
    with multipart_open_file(result_array, 'r') as files:
        temp_time_array = []  # 时间戳数组
        for file in files:  # 方法一
            if not file:  # 等价于if line == "":
                break
            line = file.readline().strip()  # 每个文件读取一行
            print(line)
            # print(datetime.datetime.strptime(line.split(',')[2], "%Y-%m-%d %H:%M:%S"))
            temp_time_array.append(line.split(',')[2])
            # temp_time_array.append(datetime.datetime.strptime(line.split(',')[2], "%Y-%m-%d %H:%M:%S"))
        # print(sort_date_list(temp_time_array, '%Y-%m-%d %H:%M:%S',False))
        DateParser().sort_date_list(temp_time_array, DateType.YMD_HMS)