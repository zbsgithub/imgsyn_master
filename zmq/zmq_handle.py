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
import logging
import os
import json

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:8080")
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
'''
获取分发机器mac
'''
def get_distribute_mac(conf_file):

#格式：mac:/data/snapshot_archives/00163E001D8F/2018-10-24

    sub_dir_array = {} #mac字典
    yesterday = datetime.datetime.now().date() - datetime.timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    # yesterday_str ="2018-10-24"

    for dir in os.listdir(conf_file["dst_path"]):
        sub_dir_array[dir] = conf_file["dst_path"]+dir+os.sep+ yesterday_str

    return sub_dir_array


'''
发送消息到队列
'''
def send_macinfo_to_queue(ci_array_log):
   mac_array=get_distribute_mac(ci_array_log)
   # while True:
   #     for mac in mac_array:
   #
   #         message = "00163E001D8F:Publish message zbs"
   #         logging.info("Publish Message: %s" % message)
   #
   #          #  Send reply back to client
   #         time.sleep(1)
   #          #mac yesterday
   #         socket.send_string("%s:%s" % (mac, mac_array[mac]))
   #         print("%s:%s" % (mac, mac_array[mac]))
   for mac in mac_array:

       message = "00163E001D8F:Publish message zbs"
       logging.info("Publish Message: %s" % message)

        #  Send reply back to client
       time.sleep(1)
        #mac yesterday
       socket.send_string("%s:%s" % (mac, mac_array[mac]))
       print("%s:%s" % (mac, mac_array[mac]))


if __name__ == '__main__':
    logging.info('--------------begin application----------------------------')
    # 读取日志文件
    file_log = open('../loggin_conf.json', 'r', encoding='utf-8')
    ci_array_log = json.load(file_log)

    send_macinfo_to_queue(ci_array_log)

    logging.info('--------------end application----------------------------')