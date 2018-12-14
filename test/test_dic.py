#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/13 11:15
# @Author  : zbs
# @Site    : 
# @File    : test_dic.py
# @Software: PyCharm

if __name__ == '__main__':
    d = {"a":11,"b":2,"c":32,"d":54}
    d['E'] = 89

    temp_dict = sorted(d.items(), key=lambda d: d[1])

    for k,v in temp_dict.__iter__():
        print(k,v)
        break