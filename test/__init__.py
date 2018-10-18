#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/12 11:16
# @Author  : Aries
# @Site    :
# @File    : __init__.py.py
# @Software: PyCharm

from gevent import monkey
import gevent
import requests
import time

monkey.patch_all()


def req(url):
    print(url)
    resp = requests.get(url)
    print(resp.status_code, url)


def synchronous_times(urls):
    """同步请求运行时间"""
    start = time.time()
    for url in urls:
        req(url)
    end = time.time()
    print('同步执行时间 {} s'.format(end - start))


def asynchronous_times(urls):
    """异步请求运行时间"""
    start = time.time()
    gevent.joinall([gevent.spawn(req, url) for url in urls])
    end = time.time()
    print('异步执行时间 {} s'.format(end - start))

urls = ['https://book.douban.com/tag/小说', 'https://book.douban.com/tag/科幻', 'https://book.douban.com/tag/漫画',
        'https://book.douban.com/tag/奇幻', 'https://book.douban.com/tag/历史', 'https://book.douban.com/tag/经济学']


if __name__ == '__main__':
  print("1ii")
  synchronous_times(urls) #同步执行时间
  # asynchronous_times(urls)