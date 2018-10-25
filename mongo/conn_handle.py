#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/17 16:02
# @Author  : zbs
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
'''
连接mongodb及处理相关查询
'''

import pymongo
import datetime

'''
建立数据库连接及创建集合
'''


def conn(method, json_obj):
    db_client = pymongo.MongoClient('mongodb://47.93.137.202:27017/')
    dblist = db_client.list_database_names()

    if "test_mongo" in dblist:  # 判断是否存在数据库test_mongo
        pass
    else:
        pass
        db_test_mongo = db_client["db_test_mongo"]  # create database testmongo
        collect_list = db_test_mongo.list_collection_names()  # all collect list
        if "test_collect" in collect_list:  # 查看集合是否存在
            # print('exist')
            test_collect = db_test_mongo["test_collect"]  # 创建集合test_collect
            if method == "insert":
                obj = test_collect.insert_one(json_obj)  # 插入数据
                print(obj.inserted_id)
                return obj
            elif method == "update":
                obj = test_collect.update_one({"did": json_obj.get("did")},
                                              {"$set": {'mac': json_obj.get("mac"),
                                                        "update_time": json_obj.get("update_time")}})
                return obj
            elif method == "query":
                result = test_collect.find_one(json_obj)  # 查询单条数据
                return result  # 创建集合test_collect
        else:
            test_collect = db_test_mongo["test_collect"]  # 创建集合test_collect
            print(test_collect.find())


'''
插入数据 
'''

# def insert(json_obj):
#     test_collect = conn()
#     obj = test_collect.insert_one(json_obj)  # 插入数据
#     print(obj.inserted_id)


'''
查询集合
'''

# def query(condition):
#     # {'did': 'python'}
#     test_collect = conn()
#     result = test_collect.find_one(condition)  # 查询单条数据
#     print(result)
#
#     return result


if __name__ == '__main__':
    print('-----------begin shell --------------------')
    # conn("insert", {"did": "fca386940c00", "mac": "00163E007D64",
    #                 "create_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    #                 "update_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    obj = conn("query", {"did": "60427f60d19f"})
    print(obj["mac"])

    # json_obj = {"did": "fca386940c00", 'mac': 'zbs_test',
    #             "update_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')};
    # update_count = conn('update', json_obj)
    # print(update_count)
    print('-----------end shell --------------------')
