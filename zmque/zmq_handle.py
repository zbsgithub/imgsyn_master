#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/17 18:11
# @Author  : Aries
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
'''
The main function:
    Queue communication handle
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
get distribute machine mac
'''
def get_distribute_mac(conf_file):

    sub_dir_array = {}
    yesterday = datetime.datetime.now().date() - datetime.timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')

    for dir in os.listdir(conf_file["dst_path"]):
        sub_dir_array[dir] = conf_file["dst_path"]+dir+os.sep+ yesterday_str

    return sub_dir_array


'''
send msg to quene
'''
def send_macinfo_to_queue(ci_array_log):
   logging.info("begin send message to quene ")
   mac_array = get_distribute_mac(ci_array_log)
   for mac in mac_array:

        #  Send reply back to client
       time.sleep(1)
        #  message format： 00163E007D64:/data/snapshot_archives/00163E007D64/2018-10-29

       socket.send_string("%s:%s" % (mac, mac_array[mac]))
       logging.info("%s:%s" % (mac, mac_array[mac]))


if __name__ == '__main__':
    logging.info('---begin application------')
    # read log config file
    file_log = open('../loggin_conf.json', 'r', encoding='utf-8')
    ci_array_log = json.load(file_log)

    send_macinfo_to_queue(ci_array_log)

    logging.info('-----end application--------')