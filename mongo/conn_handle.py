#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/17 16:02
# @Author  : zbs
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
'''
connect mongodb
'''

import pymongo
import logging
import traceback


def conn(method, json_obj):
    try:
        db_client = pymongo.MongoClient('mongodb://47.93.181.56:27017/')
        dblist = db_client.list_database_names()

        if "test_mongo" in dblist:  # check dbname(test_mongo) exist
            pass
        else:
            db_test_mongo = db_client["db_test_mongo"]  # create database testmongo
            collect_list = db_test_mongo.list_collection_names()  # all collect list
            if "test_collect" in collect_list:  # check collection exist
                test_collect = db_test_mongo["test_collect"]  # create collection test_collect
                if method == "insert":
                    obj = test_collect.insert_one(json_obj)  # insert data
                    return obj
                elif method == "update":
                    obj = test_collect.update_one({"did": json_obj.get("did")},
                                                  {"$set": {'mac': json_obj.get("mac"),
                                                            "update_time": json_obj.get("update_time")}})
                    return obj
                elif method == "query":
                    result = test_collect.find_one(json_obj)  # find one data
                    return result  # create conllection test_collect
                elif method == "queryAll":
                    result = test_collect.find(json_obj) #find all data
                    return result
            else:
                test_collect = db_test_mongo["test_collect"]  # create conllection test_collect
                test_collect.insert_one({"did": "system_genert_test_did", "mac": "123456",
                                   "create_time": "2017-04-16 21:01:35",
                                   "update_time": "2017-04-16 21:01:35"})
    except:
        logging.error(traceback.print_exc())

if __name__ == '__main__':
    # obj = conn("query", {"did": "bcec23de6f69"})

    obj = conn("queryAll", {"mac": "00163E0AA006"})

    # print(obj.__sizeof__())
    print(obj.count())
    # for i in obj:
    #     print(i)