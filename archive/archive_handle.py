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


def show_all_son_file():
    # base_path="/data/snapshots_v1/"+datetime.datetime.now().strftime('%Y-%m-%d')
    base_path="/data/snapshots_v1/2018-10-14"
    all_files_array = os.listdir(base_path)
    for file_path in all_files_array:
        print(file_path)




if __name__ == '__main__':
    show_all_son_file()
