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


def conn(method, json_obj):
    db_client = pymongo.MongoClient('mongodb://47.93.137.202:27017/')
    dblist = db_client.list_database_names()

    if "test_mongo" in dblist:  # check dbname(test_mongo) exist
        pass
    else:
        pass
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
        else:
            test_collect = db_test_mongo["test_collect"]  # create conllection test_collect

if __name__ == '__main__':
    obj = conn("query", {"did": "60427f60d19f"})

