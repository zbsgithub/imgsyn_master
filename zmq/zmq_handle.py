#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/17 18:11
# @Author  : Aries
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
'''
主要功能：
    队列通信处理
'''


import zmq
import time
import datetime

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")


while True:
    # Wait for next request from client
    message =  "123:Publish message zbs"
    print
    "Publish Message: ", message
    #  Do some 'work'
    time.sleep(1)  # Do some 'work'
    #  Send reply back to client
    # socket.send(message)
    socket.send_string(message)